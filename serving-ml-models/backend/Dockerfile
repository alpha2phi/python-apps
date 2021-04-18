FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN git clone https://github.com/deepinsight/insightface
RUN cd insightface/python-package && pip install -e .

RUN pip install -r requirements.txt

COPY . /fastapi

EXPOSE 8088

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
