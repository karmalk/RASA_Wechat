#!/usr/bin/env bash



# 默认config配置
#CUDA_VISIBLE_DEVICES=1 python -m rasa train --config configs/config.yml --domain configs/domain.yml --data data/

# bert DIET ner intent
#CUDA_VISIBLE_DEVICES=1 python -m rasa train --config configs/bert_DIET_config.yml --domain configs/domain.yml --data data/

rasa train --config configs/config.yml --domain configs/domain.yml --data data/