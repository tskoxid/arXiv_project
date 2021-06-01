FROM python:3.8

RUN apt-get update 
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-rus

RUN tesseract --list-langs
RUN tesseract -v

COPY ./ /workdir

WORKDIR /workdir

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

