#!/bin/bash

fastapi_env=env/fastapi.env
postgres_env=env/pg.env


if [ -e "$fastapi_env" ]
then
  export $(grep -v '^#' $fastapi_env | xargs)
fi

if [ -e "$postgres_env" ]
then
  export $(grep -v '^#' "$postgres_env" | xargs)
fi