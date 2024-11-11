FROM python:3.9.13-slim
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir 
EXPOSE 5000
ENTRYPOINT [ "python", "server.py" ]