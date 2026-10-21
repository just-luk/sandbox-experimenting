FROM python:3.12-alpine

RUN adduser -D -H appuser
WORKDIR /app
COPY app.py .
USER appuser

EXPOSE 8080
CMD ["python", "app.py"]
