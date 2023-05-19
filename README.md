# Timer-management-Web-App

Simple timer management web-app with database synchronization. The main goal for this web-site is to make timers that do
not depend on web-page session. If the user leaves the page, the timers of user will be loaded from the server and all
the progress and metadata will be saved.

# Instructions

## Load the submodules
Run `git submodule update --init --recursive`

## Prepare and load the env variables
Here you should set parameters that you want to have in your project. 
All the environmental variables should be stored in `/env` folder. 

Initially, in the `env` directory there are `<name>.env-example` examples with 
all possible variables for the `<name>.env` file.

There are also exist default values for all the environment variables, so you are not
obliged to set them all.

## Run scripts to generate secrets and load environmental variables

### Install python library that is used for loading environmental variables

`pip install python-dotenv`

### Generate the secret keys

`python3 env/gen_secrets.py`

### Set the environment variables

`source <(python3 env/set_env.py)`

### Make sure that you have installed docker and docker compose

### Build and run docker containers

* To build and run docker containers just use single command:

`docker-compose build && docker-compose up`
* To build the application using docker compose just run the following command:

`docker-compose build`
* To up the docker-compose build use the following command:

`docker-compose up`

### Link to the Postman collection with all the authorization requests and responses:
[![Authorization collection](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://www.postman.com/lunar-crescent-398747/workspace/timers/collection/17330906-a9586c45-c8f7-4381-aff5-8407553e7483)

### Link to the Postman collection with requests to the Custom-DB:
[![Custom-DB collection](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://www.postman.com/lunar-crescent-398747/workspace/timers/collection/27185599-408010f2-9cea-412a-90e0-72dc7b3c46be)
