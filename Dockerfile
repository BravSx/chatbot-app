FROM python:3.11-slim
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only code & startup script & templates
COPY app.py entrypoint.sh templates/ ./templates/

RUN chmod +x entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
