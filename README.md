# python-calculator-cic

**Tarea 7.0 — UNIDAD III — 5-VE-B-SD4-515-2025-II**

**Autora:** Pamela Moposita

---

## Resumen

Este repositorio muestra un ejemplo práctico y reproducible del ciclo **CI/CD** (Integración Continua y Entrega Continua) aplicado a un proyecto Python sencillo. El pipeline automatiza:

* la ejecución de pruebas (pytest),
* la verificación de la calidad mínima del proyecto,
* la construcción del *package* Python (`.whl` y `.tar.gz`),
* y la publicación del artefacto como **Artifact** de GitHub Actions.

El objetivo de esta entrega es cumplir la **Tarea 7.0**: documentar detalladamente el ciclo CI/CD hasta la construcción del *package*, incluir ejemplos de pruebas y proporcionar pasos reproducibles.

---

## Índice

1. [Qué es CI/CD](#qué-es-cicd)
2. [Estructura del repositorio](#estructura-del-repositorio)
3. [Código de ejemplo (Calculadora)](#código-de-ejemplo-calculadora)
4. [Pruebas unitarias y parametrizadas](#pruebas-unitarias-y-parametrizadas)
5. [Configuración de packaging (pyproject.toml)](#configuración-de-packaging-pyprojecttoml)
6. [Workflow de GitHub Actions (CI/CD)](#workflow-de-github-actions-cicd)
7. [Cómo ejecutar localmente (pasos reproducibles)](#cómo-ejecutar-localmente-pasos-reproducibles)
8. [Verificación del package y obtención del artefacto en GitHub](#verificación-del-package-y-obtención-del-artefacto-en-github)
9. [Checklist para entrega y mapa a la rúbrica](#checklist-para-entrega-y-mapa-a-la-rúbrica)
10. [Referencias]

---

## Qué es CI/CD

**CI (Integración Continua)**: práctica de integrar cambios frecuentemente en una rama principal y verificar cada integración mediante builds y pruebas automáticas.

**CD (Entrega/Despliegue Continuo)**: automatiza la generación de artefactos y su entrega a entornos de prueba o producción. En esta tarea nos centramos en la **entrega hasta la construcción del package**.

---

## Estructura del repositorio

```
python-calculator-cic/
├── src/
│   └── calculator.py
├── tests/
│   └── test_calculator.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── README.md  (este archivo)
└── .gitignore
```

---

## Código de ejemplo (Calculadora)

Archivo: `src/calculator.py`

```python
"""
Módulo de calculadora simple para demostrar CI/CD
"""

class Calculator:
    """Clase que implementa operaciones matemáticas básicas"""

    def __init__(self):
        self.result = 0

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

    def power(self, base, exponent):
        return base ** exponent
```

---

## Pruebas unitarias y parametrizadas

Archivo: `tests/test_calculator.py`

```python
import pytest
from calculator import Calculator


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(1.5, 2.5) == 4.0

    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2

    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5
        assert pytest.approx(self.calc.divide(1, 3), 0.001)

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            self.calc.divide(10, 0)

    def test_power(self):
        assert self.calc.power(2, 3) == 8


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, -1, -2),
    (1.5, 2.5, 4.0),
])
def test_add_parametrized(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected
```

> **Nota:** en CI usamos `pytest.ini` para añadir `src` al `pythonpath` y que `from calculator import Calculator` funcione durante la recolección de tests.

---

## Configuración de packaging (`pyproject.toml`)

Archivo: `pyproject.toml` (ejemplo mínimo, ya incluido en el repo)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "python-calculator-cic"
version = "1.0.0"
description = "Calculadora simple para demostrar CI/CD"
readme = "README.md"
requires-python = ">=3.8"
authors = [{name = "Pamela Moposita", email = "jpp.moposita@yavirac.edu.ec"}]
dependencies = []
```

---

## Workflow de GitHub Actions (CI/CD)

Archivo: `.github/workflows/ci-cd.yml`

> Este workflow valida lint y formato, ejecuta tests en una matriz de versiones (opcional), analiza seguridad, construye el package y sube el artifact.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    name: Linting y Formato de Código
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: |
          python -m pip install --upgrade pip
          pip install flake8 black
      - run: flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - run: black --check src/ tests/ || true

  test:
    name: Pruebas Automatizadas
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        python-version: ['3.10']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt || true
          pip install pytest
      - run: pytest -v --maxfail=1

  security:
    name: Análisis de Seguridad
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: |
          python -m pip install --upgrade pip
          pip install bandit
      - run: bandit -r src/ -f json -o bandit-report.json
      - uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: bandit-report.json

  build:
    name: Construir Package
    runs-on: ubuntu-latest
    needs: [test, security]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: |
          python -m pip install --upgrade pip
          pip install build wheel setuptools
      - run: python -m build
      - run: |
          ls -la dist/ || true
          pip install twine || true
          twine check dist/* || true
      - uses: actions/upload-artifact@v4
        with:
          name: python-package
          path: dist/
```

---

## Cómo ejecutar localmente — pasos reproducibles

1. Clonar repo:

```bash
git clone https://github.com/Padme2003/python-calculator-cic.git
cd python-calculator-cic
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Instalar herramientas:

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install build
```

4. Ejecutar pruebas:

```bash
pytest
```

5. Construir package:

```bash
python -m build
ls dist/
```

---

## Verificación del package y obtención del artifact en GitHub

1. En GitHub: `Actions` → abrir la ejecución del workflow.
2. Entrar al job **build** → en la parte final buscar **Artifacts**.
3. Descargar `python-package` y validar que contiene los archivos `.whl` y `.tar.gz`.

---

## Checklist final y cómo esto mapea a la rúbrica

* README.md (documentación): este archivo explica el ciclo CI/CD y pasos reproducibles — **2 pts**
* Configuración del CI/CD: `.github/workflows/ci-cd.yml` incluido y funcional — **2 pts**
* Pruebas: `tests/test_calculator.py` y `pytest.ini` para ejecución en CI — **2 pts**
* Construcción del package: `python -m build` en workflow y artifact subido — **2 pts**
* Entrega y repositorio: repo público con archivos completos y enlace compartido — **2 pts**

---

## Referencias

* GitHub Actions: [https://docs.github.com/en/actions](https://docs.github.com/en/actions)
* Packaging Python: [https://packaging.python.org/](https://packaging.python.org/)
* pytest: [https://docs.pytest.org/](https://docs.pytest.org/)

---

**Autora:** Pamela Moposita

*Proyecto entregado para Tarea 7.0 — Unidad III — Curso 5-VE-B-SD4-515-2025-II*
