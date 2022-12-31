FROM python:3.10-bullseye

COPY requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./ado_express ./ado_express

CMD [ "python", "ado_express/main.py" ]
