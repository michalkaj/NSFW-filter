FROM ubuntu:18.04

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN apt-get update #&& apt-get install -y python3.7
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install -y python3-pip
RUN yes | pip3 install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN yes| pip3 install -r requirements.txt

ENV PYTHONPATH="/usr/src/app:${PYTHONPATH}"
COPY . .
