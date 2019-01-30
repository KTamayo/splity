FROM jjanzic/docker-python3-opencv
WORKDIR /app
RUN mkdir -p ./images/{input, output, upload}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
