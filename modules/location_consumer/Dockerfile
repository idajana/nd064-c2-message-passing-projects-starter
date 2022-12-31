FROM python:3.8-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .
CMD ["python", "consumer.py"]