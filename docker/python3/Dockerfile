FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get install -y apt-utils python3 virtualenv git python3-dev \
                       libjpeg-dev zlib1g-dev build-essential \
                       postgresql-client postgresql-server-dev-all ffmpeg \
                       gettext libgdal1i

RUN useradd -m python

COPY runserver.sh /home/python/runserver.sh
RUN chmod a+x /home/python/runserver.sh

ENV LIBRARY_PATH=/lib:/usr/lib

USER python
WORKDIR /home/python/
RUN /usr/bin/virtualenv -p /usr/bin/python3 venv
RUN . /home/python/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade wheel

CMD /home/python/runserver.sh
