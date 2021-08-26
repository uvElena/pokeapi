# syntax=docker/dockerfile:1

FROM python:3.8-slim
WORKDIR /pokeapi
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY pokeapi pokeapi
COPY run.py run.py
CMD [ "python3", "run.py"]
