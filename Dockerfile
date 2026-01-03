FROM python:3.10-slim

WORKDIR /app

# Asigurăm că output-ul Python este trimis direct la terminal 
ENV PYTHONUNBUFFERED=1

# Copiem fisierul de dependende si le instalăm
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem codul sursă
COPY src/ ./src/

# Creăm folderul pentru date 
RUN mkdir -p /app/data

# Entrypoint implicit
ENTRYPOINT ["python", "src/main.py"]
