FROM bipinkrish/file-converter:latest

RUN apt install curl -y
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN apt-get update
RUN apt-get install -y cargo clang-format z3 clang
RUN apt -y install rustfmt golang-go

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
