import requests
import json
import time
#botIp = "localhost" #本机IP
botIp = "127.0.0.1" # 本机IP
#botIp = "192.168.199.128"
botPort = '5002'
def get_nlu_log(raw_text):
    rasa_nlu_url = "http://{0}:{1}/model/parse".format(botIp,botPort)

    response = requests.post(rasa_nlu_url, json={
        "text":raw_text
    })
    nlu_json = json.loads(response.content)
    nlu_intent = "intent:{}".format(nlu_json["intent"]["name"])
    entity_dict = {}
    for entity in nlu_json["entities"]:
        if "group" in entity:
            entity_dict["group"] = entity["group"]
        entity_dict[entity["entity"]] = entity["value"]
    
    return nlu_intent,entity_dict

def get_chat_content(content):
    userid = "xiaokun"
    params = {"sender":userid,"message":content}

    rasaUrl = "http://{0}:{1}/webhooks/rest/webhook".format(botIp, botPort)
    response = requests.post(
        rasaUrl, 
        data = json.dumps(params),
        headers = {'Content-Type':'application/json'}
    )
    return response.text.encode('utf-8').decode("unicode-escape")

nlu_intent,entity_dict = get_nlu_log("/restart")
result = get_chat_content("/restart")
print("初始对话状态 槽位清空 NLU_intent:{}".format(nlu_intent))
print(result)

while 1:
    input_text= input("User:")
    start_time = time.time()
    #当前句子得到的nlu结果
    nlu_intent,entity_dict = get_nlu_log(input_text)
    print("----NLU_log:[{},{}]".format(nlu_intent,entity_dict))
    # action结果
    result = get_chat_content(input_text)
    result_json = json.loads(result)
    try:
        for i in range(len(result_json)):
            bot_utterence = result_json[i]["text"]
            print("Bot:",bot_utterence)
            end_time = time.time()
            print("time:",end_time-start_time)
        print("---Action_log:",result)
    except:
        print("bug")

    if nlu_intent.split(":")[-1] == "goodbye":
        nlu_intent,entity_dict = get_nlu_log("/restart")
        result = get_chat_content("/restart")
        print("所有槽位清空----NLU_log:[{},{}]".format(nlu_intent,entity_dict))
        print(result)
        break 
