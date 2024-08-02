FROM python:3.11.9@sha256:be395e725da55bcebfacde54d58f3e14c322a068f4a1ccc4c2cc9c7f5e0adc27

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py"]
