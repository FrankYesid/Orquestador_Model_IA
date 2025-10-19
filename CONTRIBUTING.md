# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto de Orquestación ETL con Apache Airflow! Este documento proporciona pautas para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)
- [Pull Requests](#pull-requests)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Revisión](#proceso-de-revisión)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor, reporta comportamientos inaceptables.

### Nuestros Estándares

**Comportamientos que contribuyen a crear un ambiente positivo:**

- ✅ Usar lenguaje acogedor e inclusivo
- ✅ Respetar diferentes puntos de vista y experiencias
- ✅ Aceptar críticas constructivas con gracia
- ✅ Enfocarse en lo que es mejor para la comunidad
- ✅ Mostrar empatía hacia otros miembros de la comunidad

**Comportamientos inaceptables:**

- ❌ Uso de lenguaje o imágenes sexualizadas
- ❌ Trolling, comentarios insultantes o ataques personales
- ❌ Acoso público o privado
- ❌ Publicar información privada de otros sin permiso
- ❌ Otras conductas que podrían considerarse inapropiadas

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio

```bash
# Hacer fork en GitHub, luego clonar
git clone https://github.com/tu-usuario/Orquestador_Model_IA.git
cd Orquestador_Model_IA

# Agregar upstream
git remote add upstream https://github.com/original-usuario/Orquestador_Model_IA.git
```

### 2. Crear una Rama

```bash
# Actualizar main
git checkout main
git pull upstream main

# Crear rama para tu feature
git checkout -b feature/nombre-descriptivo

# O para un bugfix
git checkout -b fix/descripcion-del-bug
```

### 3. Hacer Cambios

- Escribe código limpio y bien documentado
- Sigue los estándares de código del proyecto
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 4. Commit de Cambios

```bash
# Agregar archivos
git add .

# Commit con mensaje descriptivo
git commit -m "feat: agregar nueva funcionalidad X"
```

**Formato de mensajes de commit:**

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma faltante, etc.
- `refactor:` Refactorización de código
- `test:` Agregar tests
- `chore:` Mantenimiento

### 5. Push y Pull Request

```bash
# Push a tu fork
git push origin feature/nombre-descriptivo
```

Luego, abre un Pull Request en GitHub.

## 🐛 Reportar Bugs

### Antes de Reportar

- ✅ Verifica que no sea un bug ya reportado
- ✅ Asegúrate de estar usando la última versión
- ✅ Intenta reproducir el bug en un ambiente limpio

### Cómo Reportar

Abre un issue con la siguiente información:

**Título:** Descripción breve y clara del bug

**Descripción:**
```markdown
## Descripción del Bug
[Descripción clara y concisa del bug]

## Pasos para Reproducir
1. Ir a '...'
2. Hacer clic en '...'
3. Ejecutar '...'
4. Ver error

## Comportamiento Esperado
[Qué esperabas que sucediera]

## Comportamiento Actual
[Qué sucedió realmente]

## Screenshots
[Si aplica, agregar screenshots]

## Ambiente
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python: [e.g. 3.11]
- Airflow: [e.g. 2.8.1]
- Versión del Proyecto: [e.g. 1.0.0]

## Logs
```
[Pegar logs relevantes]
```

## Información Adicional
[Cualquier otra información relevante]
```

## 💡 Sugerir Mejoras

### Antes de Sugerir

- ✅ Verifica que no exista una sugerencia similar
- ✅ Asegúrate de que la mejora sea relevante al proyecto

### Cómo Sugerir

Abre un issue con la etiqueta "enhancement":

```markdown
## Descripción de la Mejora
[Descripción clara de la mejora propuesta]

## Motivación
[Por qué esta mejora sería útil]

## Solución Propuesta
[Cómo implementarías esta mejora]

## Alternativas Consideradas
[Otras soluciones que consideraste]

## Información Adicional
[Cualquier contexto adicional]
```

## 🔄 Pull Requests

### Checklist antes de Enviar

- [ ] El código sigue los estándares del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código, especialmente en áreas complejas
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He agregado tests que prueban mi fix/feature
- [ ] Los tests nuevos y existentes pasan localmente
- [ ] He actualizado el CHANGELOG.md

### Descripción del Pull Request

```markdown
## Tipo de Cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (fix o feature que causaría que funcionalidad existente no funcione como se esperaba)
- [ ] Cambio de documentación

## Descripción
[Descripción clara de los cambios]

## Issue Relacionado
Fixes #[número del issue]

## Cómo se ha Probado
[Describe las pruebas que realizaste]

## Screenshots (si aplica)
[Agregar screenshots]

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] He realizado una auto-revisión
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He agregado tests
- [ ] Los tests pasan
```

## 📝 Estándares de Código

### Python Style Guide

Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/) con algunas excepciones:

- Longitud máxima de línea: 120 caracteres
- Usar comillas simples para strings
- Usar type hints cuando sea posible

### Ejemplo de Código

```python
"""
Módulo para procesar datos de ventas.

Este módulo contiene funciones para extraer, transformar y cargar
datos de ventas desde y hacia la base de datos.
"""

from typing import Optional, List, Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def process_sales_data(
    data: pd.DataFrame,
    filters: Optional[Dict[str, any]] = None
) -> pd.DataFrame:
    """
    Procesa datos de ventas aplicando filtros y transformaciones.
    
    Args:
        data: DataFrame con datos de ventas
        filters: Diccionario opcional con filtros a aplicar
        
    Returns:
        DataFrame procesado
        
    Raises:
        ValueError: Si el DataFrame está vacío
        
    Example:
        >>> df = pd.DataFrame({'sales': [100, 200, 300]})
        >>> result = process_sales_data(df)
    """
    if data.empty:
        raise ValueError("El DataFrame no puede estar vacío")
    
    logger.info(f"Procesando {len(data)} registros")
    
    # Aplicar filtros si existen
    if filters:
        for column, value in filters.items():
            data = data[data[column] == value]
    
    return data
```

### Linting y Formatting

Usamos las siguientes herramientas:

```bash
# Instalar herramientas
pip install black flake8 isort mypy

# Formatear código
black scripts/ dags/

# Ordenar imports
isort scripts/ dags/

# Verificar estilo
flake8 scripts/ dags/ --max-line-length=120

# Verificar tipos
mypy scripts/ dags/
```

### Estructura de Archivos

```python
# 1. Docstring del módulo
"""Descripción del módulo."""

# 2. Imports estándar
import os
import sys
from datetime import datetime

# 3. Imports de terceros
import pandas as pd
import numpy as np
from airflow import DAG

# 4. Imports locales
from config.db_config import db_config
from scripts.utils import helper_function

# 5. Constantes
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 6. Configuración de logging
logger = logging.getLogger(__name__)

# 7. Clases y funciones
class DataProcessor:
    """Clase para procesar datos."""
    pass

def main():
    """Función principal."""
    pass

# 8. Punto de entrada
if __name__ == "__main__":
    main()
```

### Documentación

- Usa docstrings para módulos, clases y funciones
- Sigue el formato Google o NumPy para docstrings
- Documenta parámetros, retornos y excepciones
- Agrega ejemplos cuando sea útil

### Tests

```python
import pytest
import pandas as pd
from scripts.transform_data import clean_data


class TestTransformData:
    """Tests para el módulo de transformación."""
    
    def test_clean_data_removes_nulls(self):
        """Verifica que clean_data elimine valores nulos."""
        # Arrange
        df = pd.DataFrame({
            'col1': [1, 2, None],
            'col2': ['a', 'b', 'c']
        })
        
        # Act
        result = clean_data(df)
        
        # Assert
        assert result['col1'].isnull().sum() == 0
    
    def test_clean_data_empty_dataframe(self):
        """Verifica que clean_data maneje DataFrames vacíos."""
        df = pd.DataFrame()
        
        with pytest.raises(ValueError):
            clean_data(df)
```

## 🔍 Proceso de Revisión

### Qué Esperamos

1. **Código de Calidad**: Limpio, legible y bien estructurado
2. **Tests**: Cobertura adecuada de tests
3. **Documentación**: Actualizada y clara
4. **Commits**: Mensajes descriptivos y atómicos
5. **Sin Conflictos**: Rebase con main antes de enviar

### Proceso de Revisión

1. Un mantenedor revisará tu PR
2. Pueden solicitar cambios
3. Realiza los cambios solicitados
4. Una vez aprobado, se hará merge

### Tiempo de Respuesta

- Issues: 1-3 días
- Pull Requests: 3-7 días

## 🎯 Áreas de Contribución

### Prioridades Actuales

- 🔴 **Alta**: Corrección de bugs críticos
- 🟡 **Media**: Nuevas funcionalidades
- 🟢 **Baja**: Mejoras de documentación

### Ideas para Contribuir

- Agregar nuevos operadores de Airflow
- Mejorar manejo de errores
- Agregar más tests
- Mejorar documentación
- Optimizar rendimiento
- Agregar ejemplos
- Traducir documentación

## 📞 Contacto

¿Preguntas sobre cómo contribuir?

- Abre un issue con la etiqueta "question"
- Únete a nuestro [Discord/Slack]
- Envía un email a [email]

## 🙏 Agradecimientos

¡Gracias por contribuir! Cada contribución, grande o pequeña, es valiosa.

---

**Recuerda**: El objetivo es aprender y mejorar juntos. No tengas miedo de hacer preguntas o cometer errores. ¡Todos estamos aquí para ayudar!
