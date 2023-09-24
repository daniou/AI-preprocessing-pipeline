FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["docker", "run", "--name", "ai_preprocessing_pipeline", "python", "main.py"]
