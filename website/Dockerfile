FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt
CMD python3 main.py