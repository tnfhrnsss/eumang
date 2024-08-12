FROM python:3.12
LABEL authors="jhsim"

WORKDIR .

ENV HOST 0.0.0.0

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "app.py"]