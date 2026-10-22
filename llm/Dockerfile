FROM ollama/ollama:latest

RUN apt-get update \
    && apt-get install --no-install-recommends -y iproute2 kmod \
    && rm -rf /var/lib/apt/lists/*
