FROM bipinkrish/file-converter:latest

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python3","main.py"]
