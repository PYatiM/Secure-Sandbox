FROM python:3.12-slim

WORKDIR /app

COPY Requirements.txt
RUN pip install --no-cache-dir -r Requirements.txt

COPY ..

RUN useradd -m sandboxuser && chown -R sandboxuser:sandboxuser /app
USER sandboxuser

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]