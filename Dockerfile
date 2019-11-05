FROM node:10 as frontend_build
WORKDIR /usr/src/app
COPY ./src/static/frontend ./
RUN npm install
RUN npm run build

FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
# USER sudo
RUN apt-get update
RUN apt-get install -y libblas-dev liblapack-dev gfortran
RUN pip3 install --user --no-cache-dir -r requirements.txt
COPY ./src ./src
COPY ./dev_env ./dev_env
COPY ./run_dev_server ./run_dev_server
COPY --from=frontend_build ./src/static/frontend ./src/static/frontend
CMD [ "./run_dev_server.sh" ]
