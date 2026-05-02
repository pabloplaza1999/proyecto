"""Configuración centralizada de la aplicación."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _parse_bool(raw_value: str | None, default: bool = False) -> bool:
    """
    Convierte una cadena de texto (como "true", "1", "yes") en un valor booleano (True/False).
    Útil para leer configuraciones del sistema operativo.
    """
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    whisper_model: str
    device: str
    cpu_compute_type: str
    cuda_compute_type: str
    allow_cpu_fallback: bool
    beam_size: int
    video_formats: tuple[str, ...]
    audio_format: str
    clean_temp_files: bool
    language: str | None


def _configure_hf_token() -> None:
    """
    Propaga el token de Hugging Face cuando existe en variables de entorno.
    Esto permite descargar modelos de IA que requieran autenticación si fuera necesario.
    """
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token


def load_config() -> AppConfig:
    """
    Carga la configuración desde variables de entorno.
    
    GUÍA DE AJUSTE DE RENDIMIENTO Y CALIDAD:
    Para ajustar la velocidad vs. calidad, modifica las variables de entorno o estos valores:
    1. MODELO: 'tiny' o 'base' para máxima velocidad. 'large-v3' para máxima precisión.
    2. BEAM SIZE: Un valor de 1 es muy rápido; 5 es el estándar; 10+ para mayor precisión en transcripciones complejas.
    3. COMPUTE TYPE: 'int8' es ideal para CPU (ahorra RAM), 'float16' es ideal para GPU (acelera la transcripción).
    """
    _configure_hf_token()

    try:
        # BEAM SIZE: 
        # - Valores más altos (ej. 10) = Mejor calidad, pero más lento.
        # - Valores más bajos (ej. 1) = Muy rápido, pero puede cometer más errores.
        beam_size = int(os.getenv("WHISPER_BEAM_SIZE", "10"))
    except ValueError:
        beam_size = 5

    return AppConfig(
        # WHISPER_MODEL: El parámetro más importante para la calidad.
        # Opciones: "tiny", "base", "small", "medium", "large-v3"
        # - "tiny/base": Ultra rápido, calidad baja.
        # - "small/medium": Equilibrio ideal.
        # - "large-v3": Calidad máxima, requiere mucha memoria (GPU).
        whisper_model=os.getenv("WHISPER_MODEL", "base"),

        # DEVICE: "cuda" para usar tarjeta de video (muy rápido), "cpu" para procesador normal.
        device=os.getenv("WHISPER_DEVICE", "cuda").lower(),

        # COMPUTE_TYPE: 
        # - "float16": Recomendado para GPU (rápido).
        # - "int8": Recomendado para CPU (menos memoria, más velocidad).
        cpu_compute_type=os.getenv("WHISPER_CPU_COMPUTE_TYPE", "int8"),
        cuda_compute_type=os.getenv("WHISPER_CUDA_COMPUTE_TYPE", "float16"),

        allow_cpu_fallback=_parse_bool(
            os.getenv("WHISPER_ALLOW_CPU_FALLBACK", "true"),
            default=True,
        ),
        beam_size=beam_size,
        video_formats=("*.mp4", "*.avi", "*.mov", "*.mkv", "*.flv", "*.wmv"),
        audio_format="wav",
        clean_temp_files=True,
        language=os.getenv("WHISPER_LANGUAGE", "es"),
    )


SUPPORTED_DEVICES = frozenset({"auto", "cpu", "cuda"})
CONFIG = load_config()

