⚡ COMIENZA AQUÍ

# 🚀 QUICKSTART - Inicia el Proyecto en 5 Minutos

Bienvenido al **Generador de Actas por Transcripción de Videos**. Este archivo te guía rápidamente para ejecutar el proyecto.

## ⏱️ 5 Pasos Rápidos

### 1️⃣ Verifica los Requisitos (30 segundos)
```bash
python --version          # Debe ser 3.9+
ffmpeg -version           # Debe funcionar
```

✅ Si ambos funcionan, continúa. Si no, ve a [INSTALACION.md](INSTALACION.md)

### 2️⃣ Instala Dependencias (2 minutos)
```bash
pip install -r requirements.txt
```

### 2.5️⃣ Si quieres usar GPU NVIDIA
Verifica primero:

```bash
nvidia-smi
```

Si funciona, ejecuta el proyecto con GPU en esta sesión de PowerShell:

```powershell
$env:WHISPER_DEVICE="cuda"
$env:WHISPER_CUDA_COMPUTE_TYPE="float16"
python transcribe_videos.py
```

### 3️⃣ Ejecuta el Programa (1 minuto)
```bash
python transcribe_videos.py
```

### 4️⃣ Selecciona Videos
- Se abrirá una ventana de diálogo
- Selecciona 1 o más videos (MP4, AVI, MOV, etc.)
- Haz clic en "Abrir"

### 5️⃣ Obtén Resultados
- Espera a que procese (10-30 min por hora de video)
- Encontrarás `{nombre_video}_acta.docx` en la carpeta

## 📚 Documentación Completa

| Archivo | Para |
|---------|------|
| [README.md](README.md) | Información completa del proyecto |
| [INSTALACION.md](INSTALACION.md) | Instalación detallada y solución de problemas |
| [GIT_GUIDE.md](GIT_GUIDE.md) | Cómo usar Git y versionamiento |
| [CHANGELOG.md](CHANGELOG.md) | Historial de cambios y versiones |

## 🔧 Configuración Rápida

El proyecto usa `auto` por defecto, pero puedes forzar el dispositivo con variables de entorno:

```python
CONFIG = {
    "WHISPER_MODEL": "base",
    "DEVICE": "auto",                  # auto, cpu, cuda
    "CPU_COMPUTE_TYPE": "int8",
    "CUDA_COMPUTE_TYPE": "float16",
    # ... más opciones
}
```

## 🆘 Problemas Rápidos

| Problema | Solución |
|----------|----------|
| **"ModuleNotFoundError"** | `pip install --force-reinstall moviepy` |
| **"ffmpeg not found"** | Ve a [INSTALACION.md](INSTALACION.md#error-ffmpeg-not-found) |
| **Muy lento** | Cambia `"WHISPER_MODEL": "tiny"` o usa GPU |
| **Video sin audio** | Verifica con VLC, algunos formatos no son compatibles |
| **No usa GPU** | Ejecuta `nvidia-smi` y luego define `WHISPER_DEVICE=cuda` |

## 💡 Consejos

- 📹 **Primera vez?** Prueba con un video corto (1-2 minutos)
- ⚙️ **Primera ejecución:** Descargará modelo (~1 GB)
- 🔄 **Múltiples videos:** Selecciona varios de una vez
- 📊 **Ver logs:** Los mensajes en la consola son detallados

## 📊 Flujo de Trabajo

```
Tu Video → Extrae Audio → Transcribe → Crea .docx
                ↓              ↓
             2 seg        10-30 min/hora
```

## 🎯 Qué Obtiene

Archivo `.docx` con contenido así:

```xml
<transcripcion>
Texto completo del audio transcrito sin ediciones...
</transcripcion>
```

Perfecto para pasarle a otra IA para análisis.

## 🔐 Control de Versiones

Este proyecto usa Git para versionamiento:

```bash
git log --oneline        # Ver versiones anteriores
git status               # Ver cambios
git diff                 # Ver qué cambió
```

Ver [GIT_GUIDE.md](GIT_GUIDE.md) para más detalles.

## 📋 Estructura del Proyecto

```
proyecto/
├── transcribe_videos.py       ← ESTE ARCHIVO EJECUTA
├── requirements.txt           ← INSTALA ESTO PRIMERO
├── README.md                  ← Lee si quieres saber más
├── INSTALACION.md             ← Si hay problemas
├── GIT_GUIDE.md               ← Cómo usar Git
├── CHANGELOG.md               ← Qué cambió
└── .git/                      ← Historial Git
```

## ✅ Verificación de Instalación

```bash
python -c "import moviepy, faster_whisper, docx; print('✓ OK')"
```

Debe mostrar: `✓ OK`

## 🚀 Listo?

```bash
python transcribe_videos.py
```

¡Eso es! El programa hace todo lo demás.

---

**¿Necesitas ayuda?**
1. Lee [INSTALACION.md](INSTALACION.md)
2. Revisa los logs en la consola (muy detallados)
3. Verifica [README.md](README.md) para más info

**¿Usarás Git para versionamiento?**
- Lee [GIT_GUIDE.md](GIT_GUIDE.md)

**¿Quieres saber qué cambió?**
- Ve [CHANGELOG.md](CHANGELOG.md)

---

**Versión:** 2.0  
**Última actualización:** 21 de abril de 2026  
**Estado:** ✅ Listo para usar
