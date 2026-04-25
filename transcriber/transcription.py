"""Módulo de transcripción con Faster Whisper."""

from __future__ import annotations

import logging
import os
from typing import Optional

from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


def transcribe_audio(audio_path: str, model: WhisperModel, beam_size: int) -> Optional[list[dict]]:
    """
    Transcribe un archivo de audio usando Faster Whisper.
    
    Retorna una lista de diccionarios, donde cada diccionario representa una frase:
    [{"start": 0.0, "end": 2.5, "text": "Hola a todos"}, ...]
    """
    try:
        logger.info("Transcribiendo audio: %s", os.path.basename(audio_path))
        
        # Esta es la llamada principal a la IA.
        segments, info = model.transcribe(audio_path, beam_size=beam_size)

        transcription_data = []
        
        # Guardamos la metadata de cada segmento para poder poner tiempos en el Word
        for segment in segments:
            transcription_data.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })

        logger.info("Transcripción completada: %s segmentos procesados", len(transcription_data))
        return transcription_data
    except FileNotFoundError as error:
        logger.error("Archivo de audio no encontrado: %s", error)
        return None
    except ValueError as error:
        logger.error("Formato de audio no soportado: %s", error)
        return None
    except Exception as error:
        logger.error("Error en transcripción: %s", error)
        return None

