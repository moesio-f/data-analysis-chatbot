FROM python:3.12-alpine

ENV MODEL="gpt-oss"
ENV PROVIDER="ollama"
ENV DATA_SOURCE_URL=""

WORKDIR /code

COPY ./chatbot/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apk add --no-cache tzdata

# Copy source code to container
COPY ./chatbot/chat chat

ENTRYPOINT ["fastapi", "run", "chat/api/api.py"]
