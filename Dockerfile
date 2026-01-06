FROM python:3.10-slim

WORKDIR /app

# Asigurăm că output-ul Python este trimis direct la terminal 
ENV PYTHONUNBUFFERED=1

# Nu avem dependinte externe, folosim doar biblioteca standard Python

# Copiem codul sursă
COPY src/ ./src/

# Creăm folderul pentru date 
RUN mkdir -p /app/data

# Entrypoint implicit
ENTRYPOINT ["python", "src/main.py"]
