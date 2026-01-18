FROM python:3.12-slim

WORKDIR /app

# Output-ul Python este trimis direct la terminal 
ENV PYTHONUNBUFFERED=1

COPY src/ ./src/

# Creăm folderul pentru date 
RUN mkdir -p /app/data

COPY src/main.py /usr/local/bin/library_manager
RUN sed -i 's/\r$//' /usr/local/bin/library_manager
RUN chmod +x /usr/local/bin/library_manager


ENTRYPOINT ["library_manager"]
