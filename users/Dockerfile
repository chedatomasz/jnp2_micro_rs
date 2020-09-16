FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80


EXPOSE 80

CMD ["flask", "run"]
