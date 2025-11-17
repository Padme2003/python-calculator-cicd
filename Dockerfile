FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY setup.py .
COPY README.md .

# Instalar la aplicación
RUN pip install -e .

# Comando por defecto
CMD ["python", "-c", "from src.calculator import Calculator; print('Calculator package installed successfully!')"]
