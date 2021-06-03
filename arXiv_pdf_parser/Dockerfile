FROM python:3.8

RUN apt-get update

COPY ./ /workdir

WORKDIR /workdir

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

