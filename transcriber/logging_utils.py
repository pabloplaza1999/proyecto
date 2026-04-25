"""Utilidades de logging."""

import logging
import os
from pathlib import Path


def configure_logging(log_file: str = "transcriber.log") -> None:
    """
    Configura cómo y dónde se guardarán los mensajes (logs) del programa.
    Muestra los mensajes en la consola en tiempo real y también los guarda en un archivo.
    """
    # Crear directorio 'logs' si no existe en la carpeta actual
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_path = log_dir / log_file
    
    # Configuración básica: formato de fecha, tipo de mensaje y texto
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Envía los mensajes a la Consola
            logging.FileHandler(log_path, encoding="utf-8")  # Guarda los mensajes en el Archivo
        ]
    )

