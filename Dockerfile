FROM pytorch/pytorch:2.2.1-cuda11.8-cudnn8-devel
USER 0
RUN apt update && apt install git -y
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir 
EXPOSE 5000
ENTRYPOINT [ "python", "server.py" ]