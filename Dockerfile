from python:3.7-slim
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install dependencies
RUN apt update -y
RUN apt install tesseract-ocr -y

WORKDIR /app
COPY code/ ./

RUN pip install -r requirement.txt
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=5", "--thread=2", "main:app"]