FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN mkdir /fastapi

COPY . /fastapi

RUN apt-get update -y

RUN apt-get install build-essential cmake protobuf-compiler python3-opencv -y

WORKDIR /fastapi

RUN pip install -r requirements.txt

EXPOSE 8088

RUN chmod +x ./start.sh

CMD ["./start.sh"]
