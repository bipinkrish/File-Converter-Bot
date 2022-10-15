FROM bipinkrish/file-converter:latest

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -y
RUN apt-get install -y cargo clang-format powershell z3 clang

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
