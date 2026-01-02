# Imaginea de bază de la care pornim 
FROM nginx:latest 
# Persoana care menține această imagine 
MAINTAINER "Numele Vostru <email@example.com>" 
# Copiem fișierele noastre în container 
COPY index.html /usr/share/nginx/html/