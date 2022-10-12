FROM bipinkrish/file-converter:latest

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
