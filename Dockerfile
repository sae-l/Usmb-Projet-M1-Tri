FROM python:3
RUN apt update
RUN apt-get -y install libpython3-dev libldap2-dev libsasl2-dev libssl-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
