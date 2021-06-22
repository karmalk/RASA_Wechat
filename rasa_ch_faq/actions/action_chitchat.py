from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted, Restarted, SlotSet,AllSlotsReset
from actions.datetime_util import datetime_to_chi,time_to_chi
from datetime import datetime, date
from actions.ChatApis import get_response

# 回答询问日期的Action 年月日
class request_datetime(Action):
    def name(self) -> Text:
        return "action_answer_requestdatetime"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        text_date = tracker.get_slot('date_time') #获取的槽位信息主要为今天明天后天
        #date_time_number = text_date_to_number_date(text_date)
        today = datetime.today()
        dayOfWeek = datetime.today().weekday()
        chi_day = "{}年{}月{}日".format(datetime_to_chi(int(today.year)),
                                     datetime_to_chi(int(today.month)),
                                     datetime_to_chi(int(today.day)))
        weekday_dict = {"0": "周一", "1": "周二", "2": "周三", "3": "周四", "4": "周五", "5": "周六", "6": "周日"}
        weekday = weekday_dict[str(dayOfWeek)]
        if text_date != "今天":
            dispatcher.utter_message("我只能给你说今天是{},查不到{}的日期".format(chi_day,text_date))
            return [UserUtteranceReverted()]
        else:
            dispatcher.utter_message("{}是{},{}".format(text_date,chi_day,weekday))
        return [UserUtteranceReverted()]

# 回答询问周几的Action
class request_weekday(Action):
    def name(self) -> Text:
        return "action_answer_requestweekday"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dayOfWeek = datetime.today().weekday()
        dayOfWeek = int(dayOfWeek)
        text_date = tracker.get_slot('date_time') #获取的槽位信息主要为今天明天后天
        if text_date == "今天":
            dayOfWeek = dayOfWeek
        elif text_date == "明天":
            if dayOfWeek == 6:
                dayOfWeek = 0
            else:
                dayOfWeek += 1
        elif text_date == "后天":
            if dayOfWeek == 6:
                dayOfWeek = 2
            elif dayOfWeek == 5:
                dayOfWeek = 0
            else:
                dayOfWeek += 2
        elif text_date == "大后天":
            if dayOfWeek == 6:
                dayOfWeek = 2
            elif dayOfWeek == 5:
                dayOfWeek = 1
            elif dayOfWeek == 4:
                dayOfWeek = 0
            else:
                dayOfWeek += 3
        else:
            dispatcher.utter_message("您问的超出我的认知范围了")
            return [UserUtteranceReverted()]
        weekday_dict = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
        weekday = weekday_dict[dayOfWeek]
        dispatcher.utter_message("{}是{}".format(text_date,weekday))
        return [UserUtteranceReverted()]

# 询问当前时间的自定义Action 无特定槽位
class request_time(Action):
    def name(self) -> Text:
        return "action_answer_time"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        from datetime import datetime
        curr_time = datetime.now()
        chi_hour = time_to_chi(curr_time.hour)
        chi_minute = time_to_chi(curr_time.minute)
        #chi_second = time_to_chi(curr_time.second)
        dispatcher.utter_message("现在是北京时间{}点{}分".format(chi_hour, chi_minute))
        return [UserUtteranceReverted()]


# 回退函数，当机器人理解不了用户的意图时，也就是当NLU的结果和Core的结果置信度都小于某个阈值的情况下，执行该Action
class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):

        # 访问图灵机器人API(闲聊)
        text = tracker.latest_message.get('text')
        utter_message = get_response(text)
        #dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        dispatcher.utter_message(utter_message)
        return [UserUtteranceReverted()]# 该返回的方法主要是为了不让intent-action mapping影响对话历史，它会删除用户的最后一条信息以及之后的一系列事件。
