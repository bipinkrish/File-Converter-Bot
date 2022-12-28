FROM bipinkrish/file-converter:latest

RUN apt install build-essential -y
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb 

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
