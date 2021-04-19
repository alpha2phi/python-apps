FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

COPY . /fastapi

RUN apt-get update -y

RUN apt-get install build-essential cmake protobuf-compiler python3-opencv -y

RUN cd /fastapi/detection/RetinaFace && make all
RUN cd /fastapi/detection/RetinaFaceAntiCov && make all

RUN pip install -r requirements.txt

EXPOSE 8088

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
