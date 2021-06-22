from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker,Action
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.WeatherApis import get_weather_by_day
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)




#获取到全部槽位信息，回复结果
class get_weather_info(Action):
    def name(self) -> Text:
        return "action_answer_weatherinfo"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        location_city = tracker.get_slot('location_city')
        date_time = tracker.get_slot('date_time')
        message_text = tracker.latest_message.get("text")

        # 规则判断输入的query中是否含有该些日期的关键词
        for item in ["今天","明天","后天","大后天"]:
            if item in message_text and date_time is None:
                date_time = item

        # 如果位置信息和时间信息都抽取出来则直接调用接口执行相关操作
        if isinstance(location_city,str) and isinstance(date_time,str):
            address= location_city
            datetime = date_time
        # 如果未从输入的query中抽取到时间信息，则默认时间为 今天
        elif location_city is None and date_time is not None:
            address = "杭州"
            datetime = date_time

        # 如果未从输入的query中抽取到位置信息，则默认地点为 杭州
        elif location_city is not None and date_time is None:
            address = location_city
            datetime = "今天"

        date_time_number = text_date_to_number_date(datetime)

        if isinstance(date_time_number, str):  # parse date_time failed
            dispatcher.utter_message("暂不支持查询 {} 的天气".format([address, date_time_number]))
            return [SlotSet("location_city", address), SlotSet("date_time", datetime)]
        else:
            weather_data = get_text_weather_date(address, datetime, date_time_number)
            dispatcher.utter_message(weather_data)
            return [SlotSet("location_city",address),SlotSet("date_time",datetime)]

        return [UserUtteranceReverted()]



def get_text_weather_date(location_city, date_time, date_time_number):
    try:
        result = get_weather_by_day(location_city, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """{} {} ({}) 的天气情况为：白天：{}；夜晚：{}；温度：{}-{} °C 湿度：{}；风向：{}；风速：{}"""
        text_message = text_message_tpl.format(
            result['location']['name'], # 地点
            date_time, # 今天/明天/后天/大后天等
            result['result']['date'], # 日期
            result['result']['text_day'], # 白天天气
            result['result']['text_night'], # 晚上天气
            result['result']["low"], # 最低温度
            result['result']["high"], # 最高温度
            result['result']["humidity"], # 湿度
            result['result']["wind_direction"], # 风向
            result['result']["wind_speed"] # 风速

        )

    return text_message


def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # TODO: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # TODO: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date
