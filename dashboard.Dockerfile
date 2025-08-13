FROM python:3.12-alpine

ENV DATA_SOURCE_URL=""
ENV CHATBOT_URL=""

WORKDIR /code

COPY ./dashboard/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apk add --no-cache tzdata

# Copy source code to container
COPY ./dashboard/app app

ENTRYPOINT ["python", "-m", "streamlit", "run", "app/entrypoint.py", "--browser.gatherUsageStats", "false"]
