FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PORT=10000

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "exec gunicorn app:server --chdir dashboard --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120"]