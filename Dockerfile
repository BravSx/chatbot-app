FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your code & startup script
COPY app.py entrypoint.sh templates/ ./ 
RUN chmod +x entrypoint.sh

# use it as the container entrypoint
ENTRYPOINT ["./entrypoint.sh"]
