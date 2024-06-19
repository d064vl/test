FROM python:3.10.5-slim-buster
WORKDIR /app
COPY *.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "storeapi.main:app", "--host" , "0.0.0.0", "--port", "8000", "--reload"]