FROM bipinkrish/file-converter:latest

RUN apt install curl -y
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN apt-get update
RUN apt-get install -y cargo clang-format z3 clang
RUN apt -y install rustfmt golang-go
RUN apt-get install openctm-tools libzbar0 -y

RUN curl -fsSL -o /tmp/warp-packer \
        https://github.com/dgiagio/warp/releases/download/v0.3.0/linux-x64.warp-packer \
    && install -D \
        --mode=755 \
        --owner=root \
        --group=root \
        /tmp/warp-packer \
        /usr/local/bin \
    && rm /tmp/warp-packer
COPY warp4j /usr/local/bin/
RUN chmod 777 /usr/local/bin/warp4j
RUN wget https://www.jflap.org/jflaptmp/july27-18/JFLAP7.1.jar && warp4j JFLAP7.1.jar  && rm -r warped/ && warp4j JFLAP7.1.jar --no-optimize && rm -r warped/ && rm JFLAP7.1.jar

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","main.py"]
