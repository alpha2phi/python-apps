FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN apt-get update

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
