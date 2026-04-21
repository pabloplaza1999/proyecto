# 📚 Guía de Git para el Proyecto

Guía rápida sobre cómo usar Git en este proyecto para versionamiento.

## 🔄 Conceptos Básicos

**Repositorio**: Copia local del proyecto con toda la historia
**Staging Area**: Área temporal donde preparas cambios
**Commit**: Captura de los cambios con descripción
**Branch**: Rama para desarrollar características sin afectar main

## 📊 Estado Actual

```bash
git status
```

Muestra:
- Archivos modificados
- Archivos nuevos sin seguimiento
- Cambios listos para commit

## 📝 Flujo de Trabajo Típico

### 1. Ver cambios
```bash
git status                    # Ver qué cambió
git diff                      # Ver diferencias en detalle
```

### 2. Preparar cambios
```bash
git add transcribe_videos.py  # Agregar archivo específico
git add -A                    # Agregar todos los cambios
```

### 3. Crear un commit
```bash
git commit -m "feat: descripción breve del cambio"
```

### 4. Ver el historial
```bash
git log                       # Ver todos los commits
git log --oneline             # Ver versión compacta
git log -p                    # Ver cambios en detalle
```

## 🏷️ Convención de Commits

Usa estos prefijos para claridad:

| Prefijo | Significado | Ejemplo |
|---------|------------|---------|
| `feat:` | Nueva característica | `feat: agregar soporte para GPU` |
| `fix:` | Corrección de error | `fix: corregir error de import` |
| `docs:` | Documentación | `docs: actualizar README` |
| `style:` | Formato (sin lógica) | `style: aplicar PEP8` |
| `refactor:` | Mejora de código | `refactor: simplificar función` |
| `perf:` | Rendimiento | `perf: optimizar transcripción` |
| `test:` | Tests | `test: agregar validación` |
| `chore:` | Configuración | `chore: actualizar dependencias` |

## 📌 Ejemplos de Commits

### Después de mejorar el código:
```bash
git add transcribe_videos.py
git commit -m "refactor: separar lógica de validación en función aparte

- Nueva función validate_video()
- Mejor manejo de errores OSError
- Logs más descriptivos"
```

### Después de corregir un bug:
```bash
git add -A
git commit -m "fix: corregir error de cierre de VideoFileClip

- Agregado bloque finally para cierre seguro
- Previene fuga de recursos en caso de error"
```

### Después de actualizar documentación:
```bash
git add README.md CHANGELOG.md
git commit -m "docs: agregar ejemplos de configuración"
```

## 🌿 Trabajar con Ramas

### Crear rama para nueva característica
```bash
git checkout -b feat/nuevo-modelo-whisper
```

### Ver ramas disponibles
```bash
git branch -a
```

### Cambiar de rama
```bash
git checkout master
```

### Mergear cambios
```bash
git merge feat/nuevo-modelo-whisper
```

## 🔍 Ver Cambios

### Comparar con versión anterior
```bash
git diff HEAD~1                # Comparar con commit anterior
git diff HEAD~2                # Comparar con 2 commits atrás
git diff 6ad1d1a              # Comparar con commit específico
```

### Ver qué cambió en un archivo
```bash
git log -p transcribe_videos.py
```

### Ver commits por autor
```bash
git log --author="Nombre"
```

## ♻️ Deshacer Cambios

### Deshacer cambios sin commit
```bash
git checkout -- transcribe_videos.py
```

### Deshacer cambios ya staging
```bash
git reset HEAD transcribe_videos.py
```

### Volver a versión anterior
```bash
git revert 6ad1d1a            # Crear nuevo commit que deshace cambios
git reset --hard 6ad1d1a      # Volver directamente (cuidado: destructivo)
```

## 📤 Compartir Cambios (Remote)

### Ver repositorio remoto
```bash
git remote -v
```

### Agregar repositorio remoto
```bash
git remote add origin https://github.com/usuario/repo.git
```

### Subir cambios
```bash
git push origin master
```

### Descargar cambios
```bash
git pull origin master
```

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Mejorar el script
```bash
# 1. Editar transcribe_videos.py
# 2. Probar los cambios
python transcribe_videos.py

# 3. Ver qué cambió
git status
git diff transcribe_videos.py

# 4. Preparar cambios
git add transcribe_videos.py

# 5. Crear commit
git commit -m "refactor: mejorar validación de video"

# 6. Ver historial
git log --oneline
```

### Ejemplo 2: Hacer cambios en rama de desarrollo
```bash
# 1. Crear rama
git checkout -b feat/soporte-cuda

# 2. Hacer cambios
# ... editar transcribe_videos.py ...

# 3. Commit en rama
git add -A
git commit -m "feat: agregar soporte para GPU CUDA"

# 4. Volver a master
git checkout master

# 5. Mergear cambios
git merge feat/soporte-cuda

# 6. Limpiar rama
git branch -d feat/soporte-cuda
```

## 📊 Tags (Etiquetas para Versiones)

### Crear tag
```bash
git tag -a v2.0 -m "Versión 2.0 con buenas prácticas"
```

### Ver tags
```bash
git tag -l
```

### Ver cambios de una versión
```bash
git show v2.0
```

## 📋 Ver Diferencia Entre Versiones

```bash
git log v1.0..v2.0          # Ver commits entre versiones
git diff v1.0 v2.0          # Ver cambios de código entre versiones
git shortlog v1.0..v2.0     # Ver resumen por autor
```

## 🚀 Mejores Prácticas

1. **Commits frecuentes**: Mejor rastrabilidad
2. **Mensajes descriptivos**: Facilita entender qué cambió
3. **Ramas para features**: Evita conflictos en master
4. **Prueba antes de commit**: Asegura código funcional
5. **Actualizar CHANGELOG.md**: Documentar cambios
6. **Usar .gitignore**: Evitar archivos innecesarios

## 🆘 Comandos Útiles

```bash
git help <comando>           # Ayuda de un comando
git stash                    # Guardar cambios temporalmente
git cherry-pick <commit>     # Aplicar commit específico
git blame <archivo>          # Ver quién cambió cada línea
git bisect                   # Buscar commit que introdujo bug
```

---

**Más información**: `git help` o [Git Documentation](https://git-scm.com/doc)
