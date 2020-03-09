FROM python:3.6

RUN  apt-get update -y && \
    apt-get upgrade -y 

# API
RUN mkdir -p /usr/src/package
COPY ./package /usr/src/package
RUN pip install -e /usr/src/package

# Deployment
RUN apt-get install supervisor -y
RUN pip install gunicorn

# Supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start processes
CMD ["/usr/bin/supervisord"]