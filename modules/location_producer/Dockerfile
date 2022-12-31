FROM python:3.8-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5005

COPY . .
RUN  python3 -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ location.proto
CMD ["python", "main.py"]