FROM soulteary/cronicle:0.9.63

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && pip3 install --no-cache-dir requests \
    && apt-get clean
