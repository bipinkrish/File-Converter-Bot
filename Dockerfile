FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get upgrade -y
RUN apt install libssl-dev
RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt install -y wget
RUN apt install zip unzip

COPY . .

CMD ["python3","fileconv.py"]
