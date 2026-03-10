FROM python:3.10.13

WORKDIR /usr/src/app

COPY . .

RUN apt-get update

RUN apt-get install -y build-essential python-dev tcpdump python-capstone libnetfilter-queue-dev libffi-dev libssl-dev

RUN python setup.py sdist

RUN pip install dist/*

CMD [ "pythem" ]

