"""Carga de modelo Whisper y utilidades de runtime CUDA/CPU."""

from __future__ import annotations

import logging
import os
import shutil
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

from faster_whisper import WhisperModel

from .config import AppConfig, SUPPORTED_DEVICES

logger = logging.getLogger(__name__)
_DLL_HANDLES = []


def is_cuda_runtime_error(error: Exception) -> bool:
    """
    Detecta si un error proviene de fallos típicos en la tarjeta de video (CUDA).
    Esto es útil para saber cuándo cambiar automáticamente a procesar con la CPU.
    """
    message = str(error).lower()
    signatures = (
        "cublas64_12.dll",
        "cudnn",
        "cuda",
        "cannot be loaded",
        "is not found",
    )
    return any(signature in message for signature in signatures)


def _configure_windows_dll_paths() -> None:
    """
    Soluciona problemas comunes en Windows donde el programa no encuentra
    los archivos (.dll) necesarios para que funcione la aceleración gráfica.
    Añade las rutas correctas al sistema.
    """
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return

    candidate_paths: list[Path] = []
    cuda_path = os.getenv("CUDA_PATH")
    if cuda_path:
        candidate_paths.append(Path(cuda_path) / "bin")

    # Add pip installed nvidia cublas/cudnn paths if they exist
    try:
        import site
        site_packages = site.getsitepackages()
        if hasattr(site, 'getusersitepackages'):
            site_packages.append(site.getusersitepackages())
            
        for site_pkg in site_packages:
            site_pkg_path = Path(site_pkg)
            cublas_bin = site_pkg_path / "nvidia" / "cublas" / "bin"
            cudnn_bin = site_pkg_path / "nvidia" / "cudnn" / "bin"
            if cublas_bin.exists():
                candidate_paths.append(cublas_bin)
            if cudnn_bin.exists():
                candidate_paths.append(cudnn_bin)
    except Exception as e:
        logger.warning("Error buscando paquetes de nvidia: %s", e)

    try:
        import ctranslate2

        candidate_paths.append(Path(ctranslate2.__file__).resolve().parent)
    except Exception:
        pass

    seen = set()
    for path in candidate_paths:
        resolved = str(path.resolve())
        if resolved in seen or not path.exists():
            continue
        try:
            handle = os.add_dll_directory(resolved)
            _DLL_HANDLES.append(handle)
            # También añadir al PATH del sistema para dependencias transitivas
            os.environ["PATH"] = resolved + os.pathsep + os.environ.get("PATH", "")
            seen.add(resolved)
        except Exception as error:
            logger.warning("No se pudo registrar ruta de DLL '%s': %s", resolved, error)


def detect_nvidia_gpu() -> str | None:
    """
    Intenta detectar automáticamente si el equipo tiene una tarjeta de video NVIDIA
    ejecutando el comando 'nvidia-smi'. Retorna el nombre de la GPU si existe.
    """
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return None

    try:
        result = subprocess.run(
            [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
        )
        gpu_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return gpu_names[0] if gpu_names else None
    except Exception as error:
        logger.warning("No se pudo consultar nvidia-smi: %s", error)
        return None


def build_model_load_attempts(config: AppConfig) -> tuple[tuple[str, str], ...]:
    """
    Decide el orden en el que se intentará cargar la IA dependiendo del equipo.
    Ej: Si pide "cuda" (GPU) pero falla, crea un plan de respaldo para usar "cpu".
    """
    requested_device = config.device
    gpu_name = detect_nvidia_gpu()

    if requested_device not in SUPPORTED_DEVICES:
        logger.warning(
            "Dispositivo no soportado en WHISPER_DEVICE: %s. Se usará 'auto'.",
            requested_device,
        )
        requested_device = "auto"

    attempts: list[tuple[str, str]] = []

    if requested_device == "cpu":
        attempts.append(("cpu", config.cpu_compute_type))
    elif requested_device == "cuda":
        if gpu_name:
            logger.info("GPU NVIDIA detectada: %s", gpu_name)
        else:
            logger.warning(
                "Se solicitó CUDA, pero no se detectó una GPU NVIDIA con nvidia-smi. "
                "Se intentará cargar igualmente."
            )
        attempts.append(("cuda", config.cuda_compute_type))
        if config.allow_cpu_fallback:
            attempts.append(("cpu", config.cpu_compute_type))
    else:
        if gpu_name:
            logger.info("GPU NVIDIA detectada: %s", gpu_name)
            attempts.append(("cuda", config.cuda_compute_type))
            if config.allow_cpu_fallback:
                attempts.append(("cpu", config.cpu_compute_type))
        else:
            logger.info("No se detectó una GPU NVIDIA utilizable. Se procesará en CPU.")
            attempts.append(("cpu", config.cpu_compute_type))

    return tuple(attempts)


def load_whisper_model(config: AppConfig) -> tuple[WhisperModel, str, str]:
    """
    Carga el modelo de IA de transcripción (Whisper) en la memoria RAM o VRAM.
    Si la carga en tarjeta gráfica falla, lo intenta automáticamente en el procesador.
    """
    _configure_windows_dll_paths()
    last_error = None

    for device, compute_type in build_model_load_attempts(config):
        try:
            logger.info(
                "Intentando cargar Whisper '%s' en %s con compute_type=%s",
                config.whisper_model,
                device,
                compute_type,
            )
            model = WhisperModel(
                config.whisper_model,
                device=device,
                compute_type=compute_type,
            )
            logger.info(
                "Modelo cargado exitosamente en %s con compute_type=%s",
                device,
                compute_type,
            )
            return model, device, compute_type
        except Exception as error:
            last_error = error
            logger.warning(
                "No fue posible cargar el modelo en %s con compute_type=%s: %s",
                device,
                compute_type,
                error,
            )

    raise RuntimeError(
        "No se pudo cargar Whisper ni en GPU ni en CPU. "
        f"Último error: {last_error}"
    )


def run_inference_smoke_test(model: WhisperModel) -> None:
    """
    Ejecuta una transcripción de prueba mínima con 1 segundo de silencio.
    Asegura que el sistema funciona correctamente antes de procesar un video real.
    """
    temp_audio_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_audio_path = temp_file.name

        with wave.open(temp_audio_path, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            silence_frame = struct.pack("<h", 0)

            for _ in range(16000):
                wav_file.writeframes(silence_frame)

        segments, _ = model.transcribe(temp_audio_path, beam_size=1)
        list(segments)
    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except OSError as error:
                logger.warning(
                    "No se pudo eliminar el archivo temporal de diagnóstico: %s",
                    error,
                )

