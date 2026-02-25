FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN useradd -m sandboxuser
USER sandboxuser

CMD ["python3", "main.py"]