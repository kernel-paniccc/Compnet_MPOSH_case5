FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
COPY pyproject.toml ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

COPY .env ./
COPY starter.py ./

EXPOSE 8081

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8081", "starter:app"]
