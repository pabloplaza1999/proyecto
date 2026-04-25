"""Procesamiento de medios: validación y extracción de audio."""

from __future__ import annotations

import logging
import os

from moviepy import VideoFileClip

logger = logging.getLogger(__name__)


def validate_video(video_path: str) -> bool:
    """
    Valida que el archivo de video existe, es accesible y no está corrupto o vacío.
    
    Retorna True si el video es válido para ser procesado, False de lo contrario.
    """
    try:
        # Comprueba si la ruta existe en el disco
        if not os.path.exists(video_path):
            logger.error("Video no encontrado: %s", video_path)
            return False

        # Comprueba si es un archivo (y no una carpeta, por ejemplo)
        if not os.path.isfile(video_path):
            logger.error("No es un archivo válido: %s", video_path)
            return False

        # Calcula el tamaño del archivo en MB para advertir si es sospechosamente pequeño
        file_size = os.path.getsize(video_path) / (1024 * 1024)
        if file_size < 1:
            logger.warning("Video muy pequeño (%.2f MB): %s", file_size, video_path)

        logger.info("Video validado: %s (%.2f MB)", os.path.basename(video_path), file_size)
        return True
    except Exception as error:
        # Captura errores de permisos o lectura
        logger.error("Error validando video %s: %s", video_path, error)
        return False


def extract_audio(video_path: str, audio_path: str) -> bool:
    """
    Extrae la pista de audio de un archivo de video y la guarda en formato WAV.
    Esto es necesario porque la IA de transcripción trabaja mejor con audios directos.
    
    Retorna True si la extracción fue exitosa, False en caso de error.
    """
    video_clip = None
    try:
        logger.info("Extrayendo audio de: %s", os.path.basename(video_path))
        # Abre el video usando la librería moviepy
        video_clip = VideoFileClip(video_path)

        # Verifica que el video realmente tenga sonido
        if video_clip.audio is None:
            logger.error("El video no tiene pista de audio: %s", video_path)
            return False

        # Escribe el audio extraído al disco duro en la ruta indicada
        video_clip.audio.write_audiofile(audio_path)
        logger.info("Audio extraído: %s", audio_path)
        return True
    except OSError as error:
        logger.error("Error de acceso a archivo al extraer audio: %s", error)
        return False
    except ValueError as error:
        logger.error("Formato de video no soportado: %s", error)
        return False
    except Exception as error:
        logger.error("Error inesperado extrayendo audio: %s", error)
        return False
    finally:
        # Asegura que el recurso del video se cierre y se libere la memoria RAM
        if video_clip is not None:
            try:
                video_clip.close()
            except Exception as error:
                logger.warning("Error cerrando VideoFileClip: %s", error)


def cleanup_temp_file(file_path: str, *, enabled: bool) -> None:
    """
    Elimina un archivo temporal (como el audio extraído) para no llenar el disco duro.
    
    Se ejecuta de forma segura: si falla o la opción está deshabilitada, no rompe el programa.
    """
    try:
        # Solo intenta borrar si la limpieza está habilitada y el archivo existe
        if enabled and os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Archivo temporal eliminado: %s", file_path)
    except OSError as error:
        logger.warning("Error al eliminar archivo temporal: %s", error)

