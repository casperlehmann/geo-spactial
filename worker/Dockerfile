FROM python:3.7.4-stretch

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
ENV APP_DIR /app
WORKDIR ${APP_DIR}

CMD ["python", "worker.py"]
