FROM ubuntu:16.04

RUN apt update && apt upgrade
#RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get -y install python2.7 python-pip git
RUN pip install --upgrade pip
ADD . /opt/fambook
WORKDIR /opt/fambook

RUN ls -l
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run_app.py"]

#symstu@symstu-HP-Pavilion-g6-Notebook-PC:~/PycharmProjects/fambook/Docker$ sudo docker build -f web-app/Dockerfile ../ -t fambook:latest
