[![CircleCI](https://circleci.com/gh/uob-spe-1617-namenotfound/IOTPlatform.svg?style=shield&circle-token=8d0cd3c5f3884fdfdbb784bf354559038c2744ff)](https://github.com/uob-spe-1617-namenotfound/IOTPlatform)


# 404.-NAMENOTFOUND
Project Repository for Software Product Engineering

## Run tests
Run `docker-compose -f test-docker-compose.yml up`

## Run application
Copy each config.example.cfg file to config.cfg in the same directory (one per service) and adapt config values if needed.

Run `docker-compose up`

## Resetting MongoDB to dummy data
Run `docker exec -it iotplatform_api_1 /bin/bash` to enter the container (assuming that the containing directory is 
named IOTPlatform, use `docker ps` to find out the name of your API container if that is not the case).

Inside the container:
* Run `export FLASK_APP=main.py`
* Run `python -m flask clear_db`
* Run `python -m flask fill_hardcoded_db`
