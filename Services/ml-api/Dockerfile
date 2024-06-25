FROM python:3.10

WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY models/ ./models
COPY scalers/ ./scalers

COPY app/ ./app
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
