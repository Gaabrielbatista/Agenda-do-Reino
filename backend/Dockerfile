FROM python:3.13.1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade head && gunicorn -w 4 -b 0.0.0.0:5000 "app.app:create_app()"