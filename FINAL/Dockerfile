# ===== Base Image =====
FROM python:3.11-slim

# ===== Set Working Directory =====
WORKDIR /app

# ===== System dependencies for LightGBM =====
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential\
    git \
    gcc \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# ===== Copy Project Files =====
COPY . .


# ===== Install Python Dependencies =====
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# ===== Expose API Port =====
EXPOSE 8000

# ===== Launch the API =====
CMD ["uvicorn", "FINAL.api:app", "--host", "0.0.0.0", "--port", "8000"]
