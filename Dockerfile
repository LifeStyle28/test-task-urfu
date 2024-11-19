FROM python:3.11

RUN apt update && \
    apt install -y git && \
    apt clean

RUN pip3.11 install omegaconf==2.3.0 && \
    pip3.11 install fastapi==0.115.5 && \
    pip3.11 install uvicorn==0.32.0 && \
    pip3.11 install requests==2.32.3 && \
    pip3.11 install aiogram

WORKDIR /app

RUN apt update && apt install -y nodejs npm

RUN git clone https://github.com/jehy/telegram-test-api.git
RUN cd telegram-test-api && npm install && npm run build
