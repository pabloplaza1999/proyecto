"""Funciones de interfaz para selección de archivos."""

from __future__ import annotations

import logging
import tkinter as tk
from collections.abc import Sequence
from tkinter import filedialog

logger = logging.getLogger(__name__)


def select_videos(video_formats: Sequence[str]) -> tuple[tuple[str, ...], bool]:
    """
    Abre un diálogo para seleccionar uno o más videos.
    
    Esta función utiliza tkinter para mostrar una ventana de selección de archivos.
    - Crea una ventana raíz oculta.
    - Define los filtros de archivos basados en los formatos permitidos.
    - Captura las rutas de los archivos seleccionados.
    - Retorna una tupla con las rutas y un booleano indicando el éxito de la operación.
    """
    try:
        # Inicializa la ventana de tkinter pero la oculta inmediatamente
        root = tk.Tk()
        root.withdraw()
        
        # Esto fuerza que el buscador de archivos aparezca por encima de todas las ventanas
        # evitando que se quede "escondido" detrás de la terminal
        root.attributes("-topmost", True)

        # Define los tipos de archivos que se mostrarán en el buscador
        filetypes = [("Archivos de video", " ".join(video_formats)), ("Todos", "*.*")]
        
        # Abre el diálogo de selección múltiple de archivos
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar videos para transcribir",
            filetypes=filetypes,
        )

        # Cierra la ventana raíz de tkinter para liberar recursos
        root.destroy()

        # Si el usuario cierra la ventana sin seleccionar nada
        if not file_paths:
            logger.info("Selección cancelada por el usuario")
            return (), False

        # Informa cuántos archivos fueron seleccionados con éxito
        logger.info("Seleccionados %s videos", len(file_paths))
        return tuple(file_paths), True
    except Exception as error:
        # Captura y registra cualquier error inesperado durante el proceso
        logger.error("Error al abrir diálogo de selección: %s", error)
        return (), False


