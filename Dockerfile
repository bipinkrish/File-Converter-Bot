FROM bipinkrish/file-converter:latest
RUN apt install iputils-ping -y

COPY . .
RUN chmod 777 c41lab.py negfix8 tgsconverter c4go
RUN chmod 777 / ~ .
RUN pip install --no-cache-dir -r requirements.txt

ENV QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"

CMD ["python3","main.py"]