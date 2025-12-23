# =============================================================================
# Dockerfile - Parco Letterario Giovanni Verga e Luigi Capuana (Production)
# =============================================================================

# 1. Immagine base con Python
FROM python:3.12-slim

# 2. Impostazioni Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Cartella di lavoro
WORKDIR /app

# 4. Pacchetti di sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Creare utente non-root per sicurezza
RUN useradd --create-home --shell /bin/bash appuser

# 6. Dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia il codice del progetto
COPY --chown=appuser:appuser . .

# 8. Creare directory per static e media
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

# 9. Passare a utente non-root
USER appuser

# 10. Espone la porta usata da Gunicorn
EXPOSE 8000

# 11. Comando di avvio (produzione con Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-", "mysite.wsgi:application"]
