FROM debian:testing

MAINTAINER Xero-Hige <Gaston.martinez.90@gmail.com>
WORKDIR /

RUN apt-get update && \
    apt-get install  -y --allow-unauthenticated --no-install-recommends build-essential && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated \
	curl \
	python3 \
	python3-pip \
	unixodbc-dev \
	libaio-dev \
	apt-transport-https \
	python3-setuptools && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN pip3 install wheel --no-cache-dir && \
    pip3 install schedule --no-cache-dir && \
    pip3 install flask --no-cache-dir && \
    pip3 install flask-cors --no-cache-dir && \
    pip3 install pyopenssl --no-cache-dir && \
    pip3 install gunicorn --no-cache-dir && \
    pip3 install python-dateutil --no-cache-dir && \
#TODO: Check version
    pip3 install mysql-connector==2.1.4 --no-cache-dir && \
    export LANG=en_US.utf-8 && \
    export LC_ALL=en_US.utf-8

WORKDIR /
COPY /src /Dantalian
COPY Dockerstart.sh /Dantalian/startscript.sh
WORKDIR /Dantalian

CMD ["bash","startscript.sh"]
