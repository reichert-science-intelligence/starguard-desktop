FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl gcc g++ \
    && rm -rf /var/lib/apt/lists/* \
    && curl -L -o /usr/local/bin/opa \
        https://github.com/open-policy-agent/opa/releases/download/v0.70.0/opa_linux_amd64_static \
    && chmod +x /usr/local/bin/opa

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
ENV PYTHONUNBUFFERED=1

CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
