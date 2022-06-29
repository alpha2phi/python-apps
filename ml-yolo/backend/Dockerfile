FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# https://stackoverflow.com/questions/55313610/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install git -y
RUN apt-get install -y procps gdb

RUN python -m pip install --upgrade pip

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt

COPY . /fastapi

EXPOSE 8088

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
