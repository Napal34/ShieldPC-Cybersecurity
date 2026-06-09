
FROM python:3.13-slim
RUN pip install --no-cache-dir psutil
WORKDIR /app
COPY cyber_shield.py .
CMD ["python", "-u", "cyber_shield.py"]
