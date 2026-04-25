"""Orquestación principal de la aplicación."""

from __future__ import annotations

import logging
from tkinter import messagebox

from faster_whisper import WhisperModel

from .config import CONFIG, AppConfig
from .logging_utils import configure_logging
from .model_runtime import (
    is_cuda_runtime_error,
    load_whisper_model,
    run_inference_smoke_test,
)
from .pipeline import process_videos
from .ui import select_videos

logger = logging.getLogger(__name__)


import dataclasses

def prompt_config(current_config: AppConfig) -> AppConfig:
    """Muestra un menú interactivo en la terminal para elegir la configuración."""
    print("\n" + "="*60)
    print(" ⚙️  PERFILES DE TRANSCRIPCIÓN ")
    print("="*60)
    print("1. ⚡ Rápida (Modelo 'base', Beam Size 1)")
    print("2. ⚖️  Equilibrada (Modelo 'small', Beam Size 5) [Recomendada]")
    print("3. 🌟 Alta Calidad (Modelo 'medium', Beam Size 5)")
    print("4. 💎 Máxima Calidad (Modelo 'large-v3', Beam Size 10) [Lento y pesado]")
    print(f"5. ⚙️  Mantener por defecto (Modelo '{current_config.whisper_model}', Beam Size {current_config.beam_size})")
    
    opcion = input("\nElige una opción (1-5) [5]: ").strip()
    
    model = current_config.whisper_model
    beam = current_config.beam_size
    
    if opcion == "1":
        model, beam = "base", 1
    elif opcion == "2":
        model, beam = "small", 5
    elif opcion == "3":
        model, beam = "medium", 5
    elif opcion == "4":
        model, beam = "large-v3", 10
    else:
        # Mantiene la original si es 5 o cualquier otra cosa
        return current_config
        
    return dataclasses.replace(current_config, whisper_model=model, beam_size=beam)

def main() -> None:
    """
    Punto de entrada principal que orquesta la ejecución.
    
    Flujo:
    1. Configura el sistema de registro (logs).
    2. Pide al usuario seleccionar perfil por terminal.
    3. Pide al usuario seleccionar videos por GUI.
    4. Carga el modelo de IA Whisper (con intentos en GPU y CPU).
    5. Procesa los videos seleccionados.
    6. Muestra resultados finales.
    """
    configure_logging()

    try:
        logger.info("%s", "=" * 60)
        logger.info("Iniciando Generador de Actas por Transcripción de Videos")
        logger.info("%s", "=" * 60)
        
        # Pide configuración interactiva
        config = prompt_config(CONFIG)
        
        # Muestra en el log qué configuración se está intentando usar
        logger.info(
            "Configuración solicitada: Modelo=%s, Beam=%s, Dispositivo=%s, CPU=%s, CUDA=%s",
            config.whisper_model,
            config.beam_size,
            config.device,
            config.cpu_compute_type,
            config.cuda_compute_type,
        )

        # PASO 1: Selección de archivos
        video_paths, success = select_videos(config.video_formats)
        if not success or len(video_paths) == 0:
            messagebox.showinfo(
                "Información",
                "No se seleccionaron videos. El programa se cerrará.",
            )
            logger.info("Programa finalizado sin procesar videos")
            return

        # PASO 2: Carga de la IA
        logger.info("Cargando modelo Whisper '%s'...", config.whisper_model)
        try:
            model, runtime_device, runtime_compute_type = load_whisper_model(config)
            logger.info(
                "Motor de transcripción listo. Dispositivo en uso=%s, compute_type=%s",
                runtime_device,
                runtime_compute_type,
            )

            # Si se carga en NVIDIA (CUDA), hacemos una prueba rápida para asegurar que funciona
            if runtime_device == "cuda":
                try:
                    logger.info("Validando inferencia CUDA con una prueba rápida...")
                    run_inference_smoke_test(model)
                    logger.info("La inferencia CUDA quedó validada correctamente")
                except Exception as error:
                    # Si falla CUDA en la prueba, intentamos pasar a CPU automáticamente
                    if config.allow_cpu_fallback and is_cuda_runtime_error(error):
                        logger.warning(
                            "CUDA fue detectado, pero falló en tiempo de inferencia. "
                            "Se volverá a CPU automáticamente. Detalle: %s",
                            error,
                        )
                        model = WhisperModel(
                            config.whisper_model,
                            device="cpu",
                            compute_type=config.cpu_compute_type,
                        )
                        runtime_device = "cpu"
                        runtime_compute_type = config.cpu_compute_type
                        logger.info(
                            "Fallback activado. Dispositivo en uso=%s, compute_type=%s",
                            runtime_device,
                            runtime_compute_type,
                        )
                    else:
                        raise
        except Exception as error:
            logger.error("Error al cargar el modelo: %s", error)
            messagebox.showerror("Error", f"Error al cargar el modelo: {error}")
            return

        # PASO 3: Procesamiento por lotes
        success_count, fail_count = process_videos(video_paths, model, config)

        # PASO 4: Resumen y despedida
        logger.info("\n%s", "=" * 60)
        logger.info("RESUMEN DE PROCESAMIENTO")
        logger.info("%s", "=" * 60)
        logger.info("Total procesados: %s", len(video_paths))
        logger.info("Éxitos: %s", success_count)
        logger.info("Fallos: %s", fail_count)
        logger.info("%s", "=" * 60)

        if success_count > 0:
            messagebox.showinfo(
                "Completado",
                "Procesamiento finalizado.\n\n"
                f"Éxitos: {success_count}\n"
                f"Fallos: {fail_count}\n\n"
                "Los archivos .docx se encuentran en la carpeta actual.",
            )
        else:
            messagebox.showerror(
                "Error",
                "No se pudieron procesar los videos.\n"
                "Revisa los logs para más información.",
            )

    except KeyboardInterrupt:
        logger.warning("Programa interrumpido por el usuario")
        messagebox.showwarning("Cancelado", "El programa fue cancelado por el usuario")
    except Exception as error:
        # Captura errores que no hayan sido manejados antes
        logger.error("Error crítico: %s", error, exc_info=True)
        messagebox.showerror("Error", f"Error crítico: {error}")

