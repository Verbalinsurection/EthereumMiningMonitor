FROM python:3.9.2

WORKDIR /emm

COPY requirements.txt .
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /emm/requirements.txt \
   && rm -rf /emm/requirements.txt

COPY src/ .

CMD [ "python", "-u", "monitor.py" ]
