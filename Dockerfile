FROM python:3.13.1-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN playwright install
RUN playwright install-deps

COPY . .

CMD ["python","-u","main.py"]