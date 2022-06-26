FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get upgrade -y
RUN apt install libssl-dev -y
RUN apt install libicu-dev libicu-dev libcairo2-dev -y
RUN apt install libtesseract-dev -y

RUN apt install libreoffice -y
RUN apt install default-jre libreoffice-java-common -y
RUN apt install imagemagick -y
RUN apt install tesseract-ocr-all -y
RUN apt install ttf-mscorefonts-installer -yes
RUN apt install ffmpeg -y
RUN apt install fontforge -y

RUN apt install -y wget
RUN apt install zip unzip -y

RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","fileconv.py"]
