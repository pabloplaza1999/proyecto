"""Pipeline de procesamiento de videos."""

from __future__ import annotations

import logging
import os

from faster_whisper import WhisperModel

from .config import AppConfig
from .documents import create_docx, create_txt
from .media import cleanup_temp_file, extract_audio, validate_video
from .transcription import transcribe_audio

logger = logging.getLogger(__name__)


def process_videos(
    video_paths: tuple[str, ...], model: WhisperModel, config: AppConfig
) -> tuple[int, int]:
    """
    Gestiona el ciclo de vida del procesamiento de una lista de videos.
    Extrae el audio, lo transcribe y genera el documento Word por cada video.
    """
    success_count = 0
    fail_count = 0

    for index, video_path in enumerate(video_paths, 1):
        try:
            logger.info("\n%s", "=" * 60)
            logger.info("Procesando video %s/%s", index, len(video_paths))
            logger.info("%s", "=" * 60)

            # Verifica si el video existe y es legible
            if not validate_video(video_path):
                fail_count += 1
                continue

            # Genera nombres de archivos basados en el video original
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_path = f"{base_name}_audio.{config.audio_format}"
            docx_path = f"{base_name}_acta.docx"

            # 1. Extracción de audio (Paso necesario para Whisper)
            if not extract_audio(video_path, audio_path):
                fail_count += 1
                continue

            # 2. Transcripción (Uso de la IA)
            # Convierte el audio extraído en una lista de segmentos estructurados con tiempo y texto
            transcription_segments = transcribe_audio(audio_path, model, config.beam_size)
            if transcription_segments is None:
                fail_count += 1
                cleanup_temp_file(audio_path, enabled=config.clean_temp_files)
                continue

            # Nombres para los documentos generados
            video_filename = os.path.basename(video_path)
            txt_path = f"{base_name}_acta.txt"

            # 3. Creación de los archivos (Word y TXT)
            # Genera el archivo .docx final con el contenido transcrito
            docx_success = create_docx(transcription_segments, docx_path, video_filename)
            txt_success = create_txt(transcription_segments, txt_path, video_filename)
            
            if not docx_success or not txt_success:
                fail_count += 1
                cleanup_temp_file(audio_path, enabled=config.clean_temp_files)
                continue

            # 4. Limpieza: Borra el audio temporal para no llenar el disco
            # Se ejecuta solo si la configuración permite la limpieza de archivos temporales
            cleanup_temp_file(audio_path, enabled=config.clean_temp_files)
            success_count += 1
            logger.info("✓ Video completado exitosamente: %s\n", docx_path)
        except Exception as error:
            logger.error("Error inesperado procesando video %s: %s", index, error)
            fail_count += 1

    return success_count, fail_count
