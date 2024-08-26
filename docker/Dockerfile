FROM python:3-alpine

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN apk add --no-cache bash

ARG UNAME=abc
ARG UID=1000
ARG GID=1000
RUN addgroup -g $GID -S $UNAME &&  adduser -u $UID -S $UNAME
USER $UNAME

#Set the timezone for the container
ENV TZ="Australia/Perth"
# GoodWe Settings
# # Example: 192.168.0.10
ENV GW_IP_ADDRESS="10.10.100.253"
#Add the port that the inverter is streaming data. This is 8899 by default.
ENV GW_PORT="8899"
# One of ET, EH, ES, EM, DT, NS, XS, BP or None to detect inverter family automatically
ENV GW_FAMILY=None
# Usually 0xf7 for ET/EH or 0x7f for DT/D-NS/XS, or None for default value
ENV GW_COMM_ADDR=None
# time in seconds - default 1
ENV GW_TIMEOUT=5
# times to retry - default 3
ENV GW_RETRIES=3
# Ready every # seconds, keep below 60
ENV GW_INTERVAL=30
# PVoutput Settings
# The System ID from pvoutput.org
ENV PVO_SYSTEMID=""
# The API key from pvoutput.org
ENV PVO_APIKEY=""
#Set the log level
ENV LOG_LEVEL="INFO"

ENTRYPOINT ["python3", "inverter.py"]
