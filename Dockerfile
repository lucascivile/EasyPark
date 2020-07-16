FROM python:alpine

WORKDIR ../EasyPark

COPY bd_scripts/relacional.sql /docker-entrypoint-initdb.d/
COPY bd_scripts/grafos.txt /docker-entrypoint-initdb.d/
COPY bd_scripts/documentos.js /docker-entrypoint-initdb.d/


