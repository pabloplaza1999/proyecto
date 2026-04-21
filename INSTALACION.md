# 🛠️ Guía de Instalación - Generador de Actas IA

Instrucciones paso a paso para instalar y configurar el proyecto en tu sistema.

## 📥 Paso 1: Clonar el Repositorio

Si el proyecto está en GitHub u otro servidor:

```bash
git clone <URL-DEL-REPOSITORIO>
cd "Generacion Actas IA"
```

Si es local (sin repositorio remoto):

```bash
cd "C:\Users\LOQ\Downloads\IA\Generacion Actas IA"
```

## 📋 Paso 2: Verificar Requisitos

### Verificar Python
```bash
python --version
```
✅ Debe mostrar **3.8 o superior**

Ejemplo: `Python 3.11.0`

### Verificar FFmpeg
```bash
ffmpeg -version
```
✅ Debe mostrar información de FFmpeg

Si no está instalado, descárgalo desde [ffmpeg.org](https://ffmpeg.org/download.html)

## 📦 Paso 3: Instalar Dependencias

### Opción A: Instalación rápida
```bash
pip install -r requirements.txt
```

### Opción B: Instalación manual (si hay problemas)
```bash
pip install moviepy==2.2.1
pip install faster-whisper==1.2.1
pip install python-docx==1.2.0
```

### Verificar instalación
```bash
python -c "import moviepy, faster_whisper, docx; print('✓ Todo instalado')"
```

✅ Debe mostrar: `✓ Todo instalado`

## 🚀 Paso 4: Ejecutar el Programa

### Opción 1: Desde PowerShell/Terminal
```bash
python transcribe_videos.py
```

### Opción 2: Doble clic en el archivo (Windows)
- Abre el Explorador de Archivos
- Navega a la carpeta del proyecto
- Haz doble clic en `transcribe_videos.py`

### Opción 3: Crear atajo (Windows)
1. Haz clic derecho en `transcribe_videos.py`
2. Selecciona "Crear atajo"
3. Coloca el atajo en tu escritorio

## 📝 Paso 5: Primera Ejecución

1. Se abrirá una ventana de diálogo
2. Selecciona un video de prueba (corto, 1-2 minutos)
3. Haz clic en "Abrir"
4. Espera a que se complete:
   - Descargará el modelo (~1 GB en primera ejecución)
   - Extraerá audio (~segundos)
   - Transcribirá (~2-5 minutos para video corto)
   - Generará el .docx

5. Verifica el archivo generado: `{nombre_video}_acta.docx`

## 🔧 Paso 6: Verificar Instalación

Crea un script de prueba `test_installation.py`:

```python
#!/usr/bin/env python
"""Script para verificar que todo está instalado correctamente."""

import sys
import subprocess

def test_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} - Necesita 3.8+")
        return False

def test_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg - OK")
        return True
    except Exception as e:
        print(f"✗ FFmpeg - No encontrado: {e}")
        return False

def test_libraries():
    libs = ['moviepy', 'faster_whisper', 'docx']
    all_ok = True
    for lib in libs:
        try:
            __import__(lib)
            print(f"✓ {lib} - OK")
        except ImportError:
            print(f"✗ {lib} - No instalado")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    print("="*50)
    print("Verificación de Instalación")
    print("="*50)
    
    checks = [
        test_python_version(),
        test_ffmpeg(),
        test_libraries(),
    ]
    
    print("="*50)
    if all(checks):
        print("✓ Todo está listo para usar")
        sys.exit(0)
    else:
        print("✗ Hay problemas de instalación")
        sys.exit(1)
```

Ejecuta:
```bash
python test_installation.py
```

## 🐛 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'moviepy'"
```bash
pip install --force-reinstall moviepy
```

### Error: "ffmpeg not found"
- Descarga FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html)
- En Windows, extrae en `C:\ffmpeg`
- Agrega al PATH: `setx PATH "%PATH%;C:\ffmpeg\bin"`

### Error: "Formato de video no soportado"
- Verifica que el video tiene audio
- Usa VLC para validar el archivo
- Intenta convertir a MP4 con FFmpeg

### Transcripción muy lenta
- Usa un modelo más pequeño en `CONFIG`
- Si tienes GPU NVIDIA, activa CUDA

## 📚 Documentación del Proyecto

- **README.md**: Guía general del proyecto
- **GIT_GUIDE.md**: Cómo usar Git
- **CHANGELOG.md**: Historial de cambios
- **requirements.txt**: Dependencias Python

## 🎓 Próximos Pasos

### 1. Leer la documentación
```bash
# Ver README
start README.md

# Ver guía de Git
start GIT_GUIDE.md
```

### 2. Configurar según necesidades
Edita `transcribe_videos.py` y modifica `CONFIG`:
```python
CONFIG = {
    "WHISPER_MODEL": "base",  # Cambia a "tiny" si es muy lento
    "DEVICE": "cpu",          # Cambia a "cuda" si tienes GPU
    # ...
}
```

### 3. Procesar tus videos
```bash
python transcribe_videos.py
```

## 🔄 Mantener el Proyecto Actualizado

```bash
# Ver cambios disponibles
git fetch origin

# Actualizar a la última versión
git pull origin main

# Ver historial
git log --oneline
```

## 💾 Crear Respaldo

```bash
# Copiar todo el proyecto
cp -r "Generacion Actas IA" "Generacion Actas IA - Respaldo"

# O usar Git
git bundle create respaldo.bundle --all
```

## ✅ Verificación Final

```bash
# Ver status
git status

# Ver último commit
git log -1

# Ver archivos
ls -la
```

---

**Problema no resuelto?** Revisa el log detallado:
```bash
python transcribe_videos.py 2>&1 | tee error_log.txt
```

El archivo `error_log.txt` contendrá información detallada del error.
