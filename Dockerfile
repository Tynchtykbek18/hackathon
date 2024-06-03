FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV_FILE=.env

WORKDIR /hakaton

RUN pip install --upgrade pip && \
    apt-get update

COPY requirements.txt /hakaton/
RUN pip install -r /hakaton/requirements.txt

COPY . .

EXPOSE 8000

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Очищаем кэш pip и временные файлы
RUN pip cache purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

CMD ["./entrypoint.sh"]