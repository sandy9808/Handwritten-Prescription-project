FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-devel
USER 0
RUN apt update && apt install -y git build-essential

# Clone and install flash-attention from the repository
RUN git clone https://github.com/Dao-AILab/flash-attention.git && \
    cd flash-attention && \
    pip install .

RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir 
EXPOSE 5000
ENTRYPOINT [ "python", "server.py" ]
