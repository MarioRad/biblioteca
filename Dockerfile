FROM python:3.9-slim
WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Instalamos uvicorn y fastapi si no están en requirements
RUN pip install uvicorn fastapi gunicorn
EXPOSE 80
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:80"]
