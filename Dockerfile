FROM bipinkrish/file-converter:latest

RUN apt install build-essential -y

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
