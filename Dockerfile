FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get upgrade -y
RUN apt install libssl-dev -y
RUN apt install libicu-dev libicu-dev libcairo2-dev -y
RUN apt install libtesseract-dev -y
RUN apt install software-properties-common -y

RUN add-apt-repository ppa:libreoffice/ppa -y
RUN apt update -y
RUN apt upgrade -y

RUN apt install wget -y
RUN apt install zip unzip -y

RUN apt install libreoffice -y
RUN apt-get install -y libreoffice-impress
RUN apt-get install -y libreoffice-draw
RUN apt-get install -y libreoffice-calc
RUN apt-get install -y libreoffice-base
RUN apt-get install -y libreoffice-writer
RUN apt-get install -y libreoffice-math
RUN apt install default-jre libreoffice-java-common -y

RUN apt install unoconv -y
RUN apt install imagemagick -y
RUN apt install tesseract-ocr-all -y
RUN apt install ffmpeg -y
RUN apt install fontforge -y
RUN wget --no-check-certificate -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","fileconv.py"]
