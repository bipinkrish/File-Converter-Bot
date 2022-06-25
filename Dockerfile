FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get upgrade -y
RUN apt install libssl-dev
RUN apt install python3-pip -y
RUN apt install libreoffice -y
RUN apt install default-jre libreoffice-java-common -y
RUN apt install -y wget
RUN apt install zip unzip

RUN wget https://github.com/bipinkrish/file-converter-telegram-bot/releases/download/binaries/binaries.zip
RUN unzip binaries.zip
RUN rm binaries.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","fileconv.py"]
