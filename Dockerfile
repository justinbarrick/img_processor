FROM python:3.5

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app
RUN python setup.py install

ENTRYPOINT [ "/usr/local/bin/python", "img_processor/img_processor.py" ]
