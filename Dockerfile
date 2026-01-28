FROM python:3.11-slim

# Imposta variabili di ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Crea directory di lavoro
WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Crea directory per i log
RUN mkdir -p /app/logs

# Espone porta (opzionale, per API future)
EXPOSE 8000

# Comando di default
CMD ["python", "main.py"]
