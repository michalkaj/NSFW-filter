FROM ubuntu:18.04
 
WORKDIR /usr/src/app/frontend

COPY . .

RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs
RUN yes | npm install
RUN yes | npm install -g @angular/cli
RUN yes | npm install @angular-devkit/build-angular
RUN yes | npm install lodash

