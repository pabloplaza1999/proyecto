"""Punto de entrada del proyecto.

Mantiene compatibilidad con `python transcribe_videos.py`
delegando la lógica al paquete `transcriber`.
"""

from transcriber.app import main


if __name__ == "__main__":
    main()
