#!/usr/bin/env bash
# 启动服务
# 1. 启动rasa server
#python -m rasa run -m ./model_file/ --port 5002 --endpoints configs/endpoints.yml --credentials configs/credentials.yml --enable-api --log-file out.log --cors "*" --debug


rasa run -m ./models/ --port 5002 --endpoints configs/endpoints.yml --credentials configs/credentials.yml --enable-api --cors "*" --debug
