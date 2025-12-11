    # 1. Imagen base de Python
    FROM python:3.12.0-slim-bookworm

    # 2. Variables de entorno
    ENV PYTHONUNBUFFERED 1
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV APP=/app

    # 3. Cambiar el directorio de trabajo
    WORKDIR $APP

    # 4. Copiar y actualizar requerimientos
    COPY requirements.txt $APP/
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt

    # 5. Copiar el resto de la aplicación
    COPY . $APP

    # 6. Exponer el puerto que usará Django
    EXPOSE 8000

    # 7. Dar permisos al entrypoint (si lo tenés)
    RUN chmod +x /app/entrypoint.sh

    # 8. Configurar entrypoint
    ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

    # 9. Comando por defecto para iniciar la app
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
