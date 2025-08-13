# Duckdb doesn't work well with musl libc
FROM python:3.12-slim-bookworm

ENV MODEL=""
ENV PROVIDER=""
ENV DATA_SOURCE_URL=""

WORKDIR /code

COPY ./chatbot/requirements.txt .

# Install dependencies
RUN apt update && apt upgrade -y && apt install -y wget && \
    pip install --no-cache-dir -r requirements.txt 

# Copy source code to container
COPY ./chatbot/chat chat

ENTRYPOINT ["fastapi", "run", "chat/api/api.py"]
