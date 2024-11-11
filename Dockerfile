FROM python:3.10-slim
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir 
EXPOSE 5000
ENTRYPOINT [ "python", "server.py" ]