#!/usr/bin/env bash
# 启动服务
# 1. 启动action server
#CUDA_VISIBLE_DEVICES=1 
rasa run actions --port 5055 --actions actions --debug


#python -m rasa run actions --port 5055 --actions actions --debug

