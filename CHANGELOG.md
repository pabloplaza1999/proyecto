# Changelog

Todos los cambios relevantes en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere al [Versionado Semántico](https://semver.org/es/).

## [2.0] - 2026-04-21

### 🆕 Agregado
- **Integración Git**: Repositorio Git para versionamiento
- **Buenas prácticas de desarrollo**:
  - Type hints en todas las funciones
  - Docstrings completos con ejemplos
  - Logging estructurado en lugar de prints
  - Manejo de excepciones específicas
- **Nuevas funciones**:
  - `validate_video()`: Validación robusta de archivos de video
  - `cleanup_temp_files()`: Limpieza de archivos temporales
  - `process_videos()`: Orquestación del procesamiento
- **Archivos de proyecto**:
  - `requirements.txt`: Gestión de dependencias
  - `README.md`: Documentación completa
  - `.gitignore`: Archivos a ignorar
  - `CHANGELOG.md`: Este archivo
- **Configuración centralizada**: `CONFIG` dict para fácil ajuste

### 🔧 Mejorado
- Rendimiento: Optimizado para videos de 1-2 horas
- Mensajes de error más descriptivos
- Información de progreso detallada
- Resumen final con estadísticas

### 🐛 Corregido
- Error: "got an unexpected keyword argument 'verbose'" en moviepy
- Importación de VideoFileClip desde moviepy directamente
- Manejo de recursos (cierre de VideoFileClip en finally)

### 📝 Documentación
- README.md con guía completa de uso
- Docstrings en todas las funciones
- Ejemplos de configuración
- Troubleshooting incluido

## [1.0] - 2026-04-17

### 🆕 Agregado
- Version inicial del proyecto
- Funcionalidad principal:
  - Selección de videos mediante interfaz gráfica
  - Extracción de audio usando moviepy
  - Transcripción con Faster Whisper
  - Generación de archivos .docx
- Características:
  - Soporte para múltiples formatos de video
  - Etiquetas XML en transcripciones
  - Limpieza automática de archivos temporales

### ⚠️ Limitaciones
- Logging básico con prints
- Manejo genérico de excepciones
- Sin type hints
- Configuración hardcoded

---

## Cómo usar este changelog

Cuando realices cambios, actualiza este archivo con:

```markdown
## [X.Y] - YYYY-MM-DD

### 🆕 Agregado
- Nueva característica

### 🔧 Mejorado
- Mejora existente

### 🐛 Corregido
- Error corregido

### ⚠️ Deprecado
- Característica que será removida

### 🗑️ Removido
- Característica removida
```

## Convenciones de commits

Usa estos prefijos para claridad:

- `feat:` - Nueva característica
- `fix:` - Corrección de bugs
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato (sin lógica)
- `refactor:` - Refactorización de código
- `perf:` - Mejoras de rendimiento
- `test:` - Cambios en tests
- `chore:` - Cambios en configuración

Ejemplo:
```bash
git commit -m "feat: agregar validación de audio en videos"
git commit -m "fix: corregir error de import en moviepy"
git commit -m "docs: actualizar README con nuevos ejemplos"
```
