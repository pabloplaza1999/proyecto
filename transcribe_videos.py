"""Script para transcribir videos a texto y generar actas en formato .docx.

Este script implementa buenas prácticas profesionales de desarrollo:
- Type hints para claridad y validación
- Docstrings completos en cada función
- Logging estructurado en lugar de prints
- Manejo de excepciones específicas
- Configuración centralizada
- Validación robusta de entrada
- Información de progreso detallada

Flujo:
1. Permite seleccionar uno o varios videos
2. Extrae el audio de cada video
3. Transcribe el audio usando Faster Whisper (modelo local, sin API)
4. Genera un archivo .docx con la transcripción envuelta en etiquetas XML

Requisitos: moviepy, faster-whisper, python-docx, tkinter
Versión: 2.0 - Buenas Prácticas de Desarrollo
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
from docx import Document
import os
import logging
from typing import Optional, Tuple

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración centralizada
CONFIG = {
    "WHISPER_MODEL": "base",  # Opciones: tiny, base, small, medium, large
    "DEVICE": "cpu",  # Opciones: cpu, cuda
    "COMPUTE_TYPE": "int8",  # Usar cuantización para velocidad
    "BEAM_SIZE": 5,  # Controla precisión vs velocidad
    "VIDEO_FORMATS": ("*.mp4", "*.avi", "*.mov", "*.mkv", "*.flv", "*.wmv"),
    "AUDIO_FORMAT": "wav",
    "CLEAN_TEMP_FILES": True,
}


def select_videos() -> Tuple[tuple, bool]:
    """Abre un diálogo para seleccionar videos.
    
    Returns:
        Tuple: (rutas_de_videos, éxito) donde éxito indica si se seleccionaron videos
    
    Example:
        >>> video_paths, success = select_videos()
        >>> if success:
        ...     print(f"Seleccionados {len(video_paths)} videos")
    """
    try:
        root = tk.Tk()
        root.withdraw()
        
        filetypes = [("Archivos de video", " ".join(CONFIG["VIDEO_FORMATS"])), 
                     ("Todos", "*.*")]
        
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar videos para transcribir",
            filetypes=filetypes
        )
        
        root.destroy()
        
        if not file_paths:
            logger.info("Selección cancelada por el usuario")
            return (), False
        
        logger.info(f"Seleccionados {len(file_paths)} videos")
        return file_paths, True
        
    except Exception as e:
        logger.error(f"Error al abrir diálogo de selección: {e}")
        return (), False


def validate_video(video_path: str) -> bool:
    """Valida que el archivo de video existe y es accesible.
    
    Args:
        video_path: Ruta del archivo de video
    
    Returns:
        bool: True si el video es válido, False en caso contrario
    
    Example:
        >>> if validate_video("video.mp4"):
        ...     print("Video válido")
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video no encontrado: {video_path}")
            return False
        
        if not os.path.isfile(video_path):
            logger.error(f"No es un archivo válido: {video_path}")
            return False
        
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        if file_size < 1:
            logger.warning(f"Video muy pequeño ({file_size:.2f} MB): {video_path}")
        
        logger.info(f"Video validado: {os.path.basename(video_path)} ({file_size:.2f} MB)")
        return True
        
    except Exception as e:
        logger.error(f"Error validando video {video_path}: {e}")
        return False


def extract_audio(video_path: str, audio_path: str) -> bool:
    """Extrae el audio de un video y lo guarda en formato WAV.
    
    Args:
        video_path: Ruta del archivo de video de entrada
        audio_path: Ruta del archivo de audio de salida
    
    Returns:
        bool: True si la extracción fue exitosa, False en caso contrario
    
    Example:
        >>> success = extract_audio("video.mp4", "audio.wav")
        >>> if success:
        ...     print("Audio extraído exitosamente")
    """
    video_clip = None
    try:
        logger.info(f"Extrayendo audio de: {os.path.basename(video_path)}")
        
        video_clip = VideoFileClip(video_path)
        
        if video_clip.audio is None:
            logger.error(f"El video no tiene pista de audio: {video_path}")
            return False
        
        video_clip.audio.write_audiofile(audio_path)
        logger.info(f"Audio extraído: {audio_path}")
        return True
        
    except OSError as e:
        logger.error(f"Error de acceso a archivo al extraer audio: {e}")
        return False
    except ValueError as e:
        logger.error(f"Formato de video no soportado: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado extrayendo audio: {e}")
        return False
    finally:
        if video_clip is not None:
            try:
                video_clip.close()
            except Exception as e:
                logger.warning(f"Error cerrando VideoFileClip: {e}")


def transcribe_audio(audio_path: str, model: WhisperModel) -> Optional[str]:
    """Transcribe un archivo de audio a texto usando Faster Whisper.
    
    Args:
        audio_path: Ruta del archivo de audio
        model: Modelo de WhisperModel cargado
    
    Returns:
        Optional[str]: Texto transcrito o None si hay error
    
    Example:
        >>> model = WhisperModel("base", device="cpu", compute_type="int8")
        >>> text = transcribe_audio("audio.wav", model)
        >>> if text:
        ...     print(f"Transcripción: {text[:100]}...")
    """
    try:
        logger.info(f"Transcribiendo audio: {os.path.basename(audio_path)}")
        
        segments, info = model.transcribe(audio_path, beam_size=CONFIG["BEAM_SIZE"])
        
        transcription = ""
        segment_count = 0
        
        for segment in segments:
            transcription += segment.text
            segment_count += 1
        
        logger.info(f"Transcripción completada: {segment_count} segmentos procesados")
        logger.info(f"Longitud del texto: {len(transcription)} caracteres")
        
        return transcription
        
    except FileNotFoundError as e:
        logger.error(f"Archivo de audio no encontrado: {e}")
        return None
    except ValueError as e:
        logger.error(f"Formato de audio no soportado: {e}")
        return None
    except Exception as e:
        logger.error(f"Error en transcripción: {e}")
        return None


def create_docx(transcription: str, output_path: str) -> bool:
    """Crea un documento .docx con la transcripción envuelta en etiquetas XML.
    
    Args:
        transcription: Texto transcrito
        output_path: Ruta del archivo .docx de salida
    
    Returns:
        bool: True si se creó correctamente, False en caso contrario
    
    Note:
        El texto se envuelve en etiquetas <transcripcion> para que pueda
        ser procesado por otras herramientas de IA sin ambigüedad.
    
    Example:
        >>> success = create_docx("Texto transcrito", "acta.docx")
        >>> if success:
        ...     print("Documento creado exitosamente")
    """
    try:
        if not transcription or not transcription.strip():
            logger.warning("Transcripción vacía, creando documento vacío")
        
        doc = Document()
        
        # Agregar transcripción envuelta en etiquetas XML
        formatted_text = f"<transcripcion>{transcription}</transcripcion>"
        doc.add_paragraph(formatted_text)
        
        # Guardar documento
        doc.save(output_path)
        
        file_size = os.path.getsize(output_path) / 1024  # KB
        logger.info(f"Documento creado: {output_path} ({file_size:.2f} KB)")
        
        return True
        
    except IOError as e:
        logger.error(f"Error al escribir archivo .docx: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado creando .docx: {e}")
        return False


def cleanup_temp_files(audio_path: str) -> None:
    """Elimina archivos temporales (audio).
    
    Args:
        audio_path: Ruta del archivo temporal a eliminar
    
    Example:
        >>> cleanup_temp_files("audio_temp.wav")
    """
    try:
        if CONFIG["CLEAN_TEMP_FILES"] and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Archivo temporal eliminado: {audio_path}")
    except OSError as e:
        logger.warning(f"Error al eliminar archivo temporal: {e}")


def process_videos(video_paths: Tuple[str], model: WhisperModel) -> Tuple[int, int]:
    """Procesa una lista de videos: extrae audio, transcribe y crea actas.
    
    Args:
        video_paths: Tupla de rutas de videos
        model: Modelo de WhisperModel cargado
    
    Returns:
        Tuple: (éxitos, fracasos) - cantidad de videos procesados exitosamente y fallidos
    
    Example:
        >>> model = WhisperModel("base", device="cpu", compute_type="int8")
        >>> success_count, fail_count = process_videos(("video1.mp4", "video2.mp4"), model)
        >>> print(f"Procesados: {success_count}, Fallidos: {fail_count}")
    """
    success_count = 0
    fail_count = 0
    
    for index, video_path in enumerate(video_paths, 1):
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Procesando video {index}/{len(video_paths)}")
            logger.info(f"{'='*60}")
            
            # Validar video
            if not validate_video(video_path):
                fail_count += 1
                continue
            
            # Definir rutas
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            audio_path = f"{base_name}_audio.{CONFIG['AUDIO_FORMAT']}"
            docx_path = f"{base_name}_acta.docx"
            
            # Extraer audio
            if not extract_audio(video_path, audio_path):
                fail_count += 1
                continue
            
            # Transcribir
            transcription = transcribe_audio(audio_path, model)
            if transcription is None:
                fail_count += 1
                cleanup_temp_files(audio_path)
                continue
            
            # Crear documento
            if not create_docx(transcription, docx_path):
                fail_count += 1
                cleanup_temp_files(audio_path)
                continue
            
            # Limpiar archivos temporales
            cleanup_temp_files(audio_path)
            
            success_count += 1
            logger.info(f"✓ Video completado exitosamente: {docx_path}\n")
            
        except Exception as e:
            logger.error(f"Error inesperado procesando video {index}: {e}")
            fail_count += 1
    
    return success_count, fail_count


def main() -> None:
    """Función principal del programa.
    
    Orquesta el flujo:
    1. Carga el modelo de Whisper
    2. Permite seleccionar videos
    3. Procesa cada video
    4. Muestra resumen de resultados
    
    Example:
        >>> main()
    """
    try:
        logger.info("="*60)
        logger.info("Iniciando Generador de Actas por Transcripción de Videos")
        logger.info("="*60)
        logger.info(f"Configuración: Modelo={CONFIG['WHISPER_MODEL']}, "
                   f"Dispositivo={CONFIG['DEVICE']}, "
                   f"Precisión={CONFIG['COMPUTE_TYPE']}")
        
        # Seleccionar videos
        video_paths, success = select_videos()
        if not success or len(video_paths) == 0:
            messagebox.showinfo("Información", 
                              "No se seleccionaron videos. El programa se cerrará.")
            logger.info("Programa finalizado sin procesar videos")
            return
        
        # Cargar modelo
        logger.info(f"Cargando modelo Whisper '{CONFIG['WHISPER_MODEL']}'...")
        try:
            model = WhisperModel(
                CONFIG["WHISPER_MODEL"],
                device=CONFIG["DEVICE"],
                compute_type=CONFIG["COMPUTE_TYPE"]
            )
            logger.info("Modelo cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            messagebox.showerror("Error", 
                               f"Error al cargar el modelo: {e}")
            return
        
        # Procesar videos
        success_count, fail_count = process_videos(video_paths, model)
        
        # Resumen
        logger.info("\n" + "="*60)
        logger.info("RESUMEN DE PROCESAMIENTO")
        logger.info("="*60)
        logger.info(f"Total procesados: {len(video_paths)}")
        logger.info(f"Éxitos: {success_count}")
        logger.info(f"Fallos: {fail_count}")
        logger.info("="*60)
        
        # Mensaje final
        if success_count > 0:
            messagebox.showinfo(
                "Completado",
                f"Procesamiento finalizado.\n\n"
                f"Éxitos: {success_count}\n"
                f"Fallos: {fail_count}\n\n"
                f"Los archivos .docx se encuentran en la carpeta actual."
            )
        else:
            messagebox.showerror(
                "Error",
                f"No se pudieron procesar los videos.\n"
                f"Revisa los logs para más información."
            )
    
    except KeyboardInterrupt:
        logger.warning("Programa interrumpido por el usuario")
        messagebox.showwarning("Cancelado", "El programa fue cancelado por el usuario")
    except Exception as e:
        logger.error(f"Error crítico: {e}", exc_info=True)
        messagebox.showerror("Error", f"Error crítico: {e}")


if __name__ == "__main__":
    main()
