from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from service.normalization import text_to_date
from service.weather import get_text_weather_date
from service.chatBot import get_response


class WeatherFormAction(Action):
    def name(self) -> Text:
        return "action_weather_form_submit"

    def run(
        self, dispatch: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        city = tracker.get_slot("address")
        date_text = tracker.get_slot("date-time")

        date_object = text_to_date(date_text)

        if not date_object:  # parse date_time failed
            msg = "暂不支持查询 {} 的天气".format([city, date_text])
            dispatch.utter_message(msg)
        else:
            try:
                weather_data = get_text_weather_date(city, date_object, date_text)
            except Exception as e:
                exec_msg = str(e)
                dispatch.utter_message(exec_msg)
            else:
                tracker.slots.clear()
                print(tracker.slots)
                dispatch.utter_message(weather_data)

        return []


class ChatBotAction(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self, dispatch: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:

        try:
            mag = get_response(tracker.latest_message['text'])
        except Exception as e:
            exec_msg = str(e)
            dispatch.utter_message(exec_msg)
        else:
            dispatch.utter_message(mag)

        return [UserUtteranceReverted()]