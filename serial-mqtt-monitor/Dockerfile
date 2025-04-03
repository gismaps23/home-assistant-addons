FROM python:3.11-slim

WORKDIR /app

COPY run.sh .
COPY TEST34COPY.PY .

RUN pip install pyserial paho-mqtt \
 && chmod +x run.sh

CMD ["./run.sh"]
