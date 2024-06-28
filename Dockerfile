FROM python:3.9

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmysqlclient-dev \
    gcc

WORKDIR /app

COPY req.txt .

RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
