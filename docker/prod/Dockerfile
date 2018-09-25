FROM debian:buster-slim

RUN mkdir /salic-ml
WORKDIR /salic-ml

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-pyodbc \
        tdsodbc \
        unixodbc \
        gunicorn3 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

ADD ./setup.py /salic-ml/
ADD ./docker/odbcinst.ini /etc/odbcinst.ini

RUN mkdir /salic-ml/salicml
ADD ./salicml/__init__.py /salic-ml/salicml/

RUN python3 setup.py develop

EXPOSE 5000
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8
CMD ["sh", "./docker/prod/cmd.sh"]

ADD . /salic-ml/
