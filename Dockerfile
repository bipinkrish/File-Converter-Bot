FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get upgrade -y
RUN apt install libssl-dev libtesseract-dev libicu-dev libicu-dev libcairo2-dev freeglut3 freeglut3-dev libopengl0 -y

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get install -y tzdata
RUN apt install wget -y
RUN apt install zip unzip -y

RUN apt install libreoffice -y
RUN apt install default-jre libreoffice-java-common -y
RUN apt install imagemagick -y
RUN apt install tesseract-ocr-all -y
RUN apt install ffmpeg -y
RUN apt install fontforge -y
RUN apt install calibre -y

RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN apt-get install -y python3-numpy python3-pydot python3-matplotlib python3-opencv python3-graphviz python3-toolz
RUN wget https://github.com/bipinkrish/Colorize-Positive-Bot/releases/download/Model/model.zip && unzip model.zip && rm model.zip

CMD ["python3","fileconv.py"]
