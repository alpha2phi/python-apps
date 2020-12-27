
FROM python:3.8-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

RUN apt-get update -y && apt-get install nodejs npm -y 

RUN npm i -g nodemon

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]