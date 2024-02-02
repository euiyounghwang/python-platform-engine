FROM python:3.8

# COPY py_hitl_exporter.py /app/py_hitl_exporter.py
COPY py_http_export.py /app/py_http_export.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ENV HITL_URL $HITL_URL
# CMD ["python3", "/app/py_http-poll-export.py"]
CMD ["python3", "/app/py_http_export.py"]

# docker build -t euiyoung/py-http-exporter .
# docker run -p 19000:9000 -e URL=http://host.docker.internal:8888/es/health euiyoung/py-http-exporter