FROM debian:testing

MAINTAINER Xero-Hige <Gaston.martinez.90@gmail.com>
WORKDIR /

RUN apt-get update && \
    apt-get install  -y --allow-unauthenticated --no-install-recommends build-essential && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated &&\
    apt-get install -y netcat-openbsd \
	curl \
	python3 \
	python3-pip \
	unixodbc-dev \
	libaio-dev \
	apt-transport-https \
	python3-setuptools && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY requirements.txt /

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt --no-cache-dir

#FIXME: DO NOT PUSH THIS ON MASTER
RUN pip3 install coverage --no-cache-dir && \
    pip3 install requests --no-cache-dir
#FIXME: REMOVE

RUN export LANG=en_US.utf-8

WORKDIR /
COPY /src /Dantalian
COPY Dockerstart.sh /Dantalian/startscript.sh
WORKDIR /Dantalian

#FIXME: DO NOT PUSH THIS ON MASTER
COPY /testing /Testing
#FIXME: REMOVE

CMD ["bash","startscript.sh"]