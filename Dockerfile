FROM python:3.11-slim

WORKDIR /app

# 1) Install your Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy only code & startup script
COPY app.py entrypoint.sh templates/ ./

RUN chmod +x entrypoint.sh
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
