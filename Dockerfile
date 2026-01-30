FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY src/ ./src/

# Creăm folderul pentru date 
RUN mkdir -p /app/data

# Creăm comanda 'library_manager' pentru a putea fi apelată din shell
RUN echo '#!/bin/sh\npython /app/src/main.py "$@"' > /usr/local/bin/library_manager && \
    chmod +x /usr/local/bin/library_manager

ENTRYPOINT ["python", "src/main.py"]

# Comanda default care va fi afișată dacă nu se dau argumente
CMD ["--help"]
