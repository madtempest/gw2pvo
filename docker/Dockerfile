FROM python:3.7
ENV TZ="Europe/Athens"
RUN pip install goodwe requests

COPY . .

ENTRYPOINT ["python3", "inverter.py"]
