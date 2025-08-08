# Menggunakan base image python 3.11 slim
FROM python:3.11-slim

# Menetapkan direktori kerja
WORKDIR /app

# Mengatur variabel lingkungan
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app/app.py

# Menginstal dependensi sistem
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Menyalin dan menginstal dependensi python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin kode aplikasi dan tes
COPY app/ ./app/
COPY tests/ ./tests/

# Membuat user non-root untuk keamanan
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Mengekspos port aplikasi
EXPOSE 5000

# Memperbaiki perintah HEALTHCHECK dengan menghapus "|| exit 1"
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health

# Perintah untuk menjalankan aplikasi
CMD ["python", "-m", "app.app"]
