FROM python:3.12-alpine

ENV DATABASE_URL=""

WORKDIR /code

COPY ./data-sources/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apk add --no-cache tzdata

# Copy source code to container
COPY ./data-sources/app app

ENTRYPOINT ["fastapi", "run", "app/api/api.py"]
