# 📹 Generador de Actas por Transcripción de Videos

Herramienta profesional para transcribir videos a texto y generar actas en formato `.docx` con transcripciones envueltas en etiquetas XML.

## 🎯 Características

- ✅ **Transcripción local**: Usa Faster Whisper (modelo OpenAI optimizado)
- ✅ **Sin APIs de pago**: Procesamiento completamente local
- ✅ **Múltiples videos**: Procesa varios videos en una sola ejecución
- ✅ **Formato XML**: Transcripciones envueltas en `<transcripcion>` para compatibilidad con IA
- ✅ **Logging detallado**: Información completa de cada paso
- ✅ **Validación robusta**: Verifica formatos y errores específicos
- ✅ **Interfaz gráfica**: Diálogo para seleccionar videos
- ✅ **Rápido**: Procesamiento optimizado para videos largos (1-2 horas)

## 📋 Requisitos Previos

### Sistema Operativo
- Windows 10/11, macOS, o Linux

### Software Requerido
- **Python 3.8+** - [Descargar](https://www.python.org/downloads/)
- **FFmpeg** - Ya instalado en tu sistema

### Capacidad del Sistema
- CPU: 4+ núcleos (recomendado)
- RAM: 4+ GB
- Disco: 2-3 GB libres (para modelo y archivos temporales)

## 🚀 Instalación Rápida

### 1. Clonar o descargar el repositorio
```bash
git clone <url-del-repositorio>
cd "Generacion Actas IA"
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python transcribe_videos.py
```

## 📖 Uso

1. **Ejecuta el script**:
   ```bash
   python transcribe_videos.py
   ```

2. **Selecciona los videos**:
   - Se abrirá un diálogo
   - Selecciona uno o varios videos (MP4, AVI, MOV, MKV, FLV, WMV)
   - Haz clic en "Abrir"

3. **Espera el procesamiento**:
   - Extracción de audio (~segundos)
   - Transcripción (~10-30 min por hora de video)
   - Generación de documento

4. **Archivos generados**:
   - `{nombre_video}_acta.docx` en la misma carpeta

## 📄 Salida Esperada

El archivo `.docx` contiene:
```xml
<transcripcion>Aquí va el texto completo transcrito del audio...</transcripcion>
```

Sin preámbulos, resúmenes ni texto adicional.

## ⚙️ Configuración

Edita `transcribe_videos.py` para cambiar:

```python
CONFIG = {
    "WHISPER_MODEL": "base",      # tiny, base, small, medium, large
    "DEVICE": "cpu",               # cpu, cuda (si tienes GPU NVIDIA)
    "COMPUTE_TYPE": "int8",        # Cuantización para velocidad
    "BEAM_SIZE": 5,                # Mayor = más preciso pero lento
    "CLEAN_TEMP_FILES": True,      # Limpiar archivos temporales
}
```

### Modelos disponibles y tiempos aproximados
| Modelo | Tamaño | Velocidad | Precisión | RAM |
|--------|--------|-----------|-----------|-----|
| tiny   | 39 MB  | ⚡⚡⚡ Muy rápido | ⭐ Media | 1 GB |
| base   | 141 MB | ⚡⚡ Rápido | ⭐⭐⭐ Buena | 2 GB |
| small  | 466 MB | ⚡ Normal | ⭐⭐⭐ Buena | 3 GB |
| medium | 1.5 GB | ⏱️ Lento | ⭐⭐⭐⭐ Excelente | 5 GB |

Para videos de 1-2 horas, usa **base** (por defecto).

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install --force-reinstall moviepy faster-whisper python-docx
```

### Error: "El video no tiene pista de audio"
- Verifica el video con VLC
- Algunos formatos pueden no ser compatibles

### Transcripción lenta
- Usa un modelo más pequeño: cambia `"WHISPER_MODEL": "tiny"`
- Si tienes GPU NVIDIA: cambia `"DEVICE": "cuda"`

### Archivo .docx corrupto
- Intenta con un video de prueba más corto
- Verifica el espacio en disco

## 📊 Estructura del Proyecto

```
Generacion Actas IA/
├── transcribe_videos.py       # Script principal
├── transcribe_videos_v2.py    # Respaldo (versión mejorada)
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
├── CHANGELOG.md               # Historial de cambios
├── .gitignore                 # Archivos a ignorar en Git
└── .git/                      # Repositorio Git
```

## 📝 Logging

El script registra toda la información en la consola:

```
2026-04-21 17:45:00,123 - INFO - Iniciando Generador de Actas
2026-04-21 17:45:05,456 - INFO - Seleccionados 2 videos
2026-04-21 17:45:10,789 - INFO - Cargando modelo Whisper 'base'...
2026-04-21 17:45:20,000 - INFO - Modelo cargado exitosamente
2026-04-21 17:45:21,111 - INFO - ============================================================
2026-04-21 17:45:21,222 - INFO - Procesando video 1/2
2026-04-21 17:45:22,333 - INFO - Video validado: video1.mp4 (125.50 MB)
```

## 🔐 Mejores Prácticas Implementadas

- ✅ **Type hints**: Especificación clara de tipos
- ✅ **Docstrings**: Documentación en cada función
- ✅ **Logging**: Rastrabilidad completa de la ejecución
- ✅ **Manejo de excepciones**: Errores específicos y diagnósticos
- ✅ **Validación de entrada**: Verificación robusta de archivos
- ✅ **Configuración centralizada**: Fácil ajuste de parámetros
- ✅ **Control de versiones**: Git para versionamiento

## 🤝 Desarrollo

### Ver versiones anteriores
```bash
git log --oneline
```

### Ver cambios
```bash
git diff
```

### Actualizar con nuevos cambios
```bash
git pull origin main
```

## 📜 Licencia

MIT License - Uso libre para proyectos personales y comerciales

## 📞 Soporte

Para reportar errores o sugerencias, consulta los logs de ejecución para más información.

## 🎓 Créditos

- **Faster Whisper**: [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- **MoviePy**: [moviepy/moviepy](https://github.com/Zulko/moviepy)
- **python-docx**: [python-openxml/python-docx](https://github.com/python-openxml/python-docx)

---

**Versión**: 2.0 - Buenas Prácticas de Desarrollo + Git Integration
**Última actualización**: 21 de abril de 2026
