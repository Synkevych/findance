FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt

# you should provide valid credential in constants.py, example is constants.py.example
ADD constants.py /
ADD main.py /
ADD responses.py /

CMD [ "python", "./main.py" ]
