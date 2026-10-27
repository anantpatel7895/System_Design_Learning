# 1️⃣ Use slim Python image
FROM python:3.11-slim

# 2️⃣ Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set work directory
WORKDIR /app

# 4️⃣ Install system dependencies (minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copy dependency list first (for caching)
COPY requirements.txt .

# 6️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7️⃣ Copy application code
COPY app ./app

# 8️⃣ Expose port
EXPOSE 8000

# 9️⃣ Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
