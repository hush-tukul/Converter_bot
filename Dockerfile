FROM python:3.10-slim

ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-draw \
    libreoffice-math \
    libreoffice-base \
    fonts-opensymbol \
    fonts-dejavu \
    fonts-freefont-ttf \
    fonts-liberation \
    fonts-noto \
    fonts-crosextra-caladea \
    fonts-crosextra-carlito \
    ffmpeg \
    libsm6 \
    libxext6 \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-script-latn \
    libtesseract-dev \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
