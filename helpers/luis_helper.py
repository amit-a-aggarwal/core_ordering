# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from ordering_details import OrderingDetails
import json

class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    ORDER_STATUS = "OrderStatus"
    ORDER_TRACKING = "OrderTracking"
    CANCEL = "Cancel"
    GET_WEATHER = "GetWeather"
    INFORM = 'Inform'
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None
        # print("inside execute_luis_query")
        try:
            #{"text":"what is the status of my order?", "entities": {"email":"amit.a.aggarwal@pwc.com", "orderid":"OD222222"}}
            #{"text":"what is the status of my order?", "entities": {"email":"amit.a.aggarwal@pwc.com"}}
            #Response from azure : {“text”: “Your order is under processing”, “entities”: {“email”: “amit.a.aggarwal@pwc.com”, “orderid”: “od22”}}


            entities_flag = 0
            obj = None
            if '{' in turn_context.activity.text:
                # print("entered { condition")
                entities_flag = 1
                obj = json.loads(turn_context.activity.text)
                turn_context.activity.text = obj["text"]

            # print("turn_context.activity.text: ", turn_context.activity.text)
            recognizer_result = await luis_recognizer.recognize(turn_context)
            # print("recognizer_result: ", recognizer_result.__str__())

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )
            # print("intent is: ", intent)
            if intent == Intent.ORDER_STATUS.value or intent == Intent.ORDER_TRACKING.value or intent == Intent.INFORM.value:
                # result = BookingDetails()
                result = OrderingDetails()
                if entities_flag == 1:
                    for(k,v) in obj["entities"].items():
                        # print("key and value : ", k, "  ", v)
                        if k in result.__dict__.keys():
                            key = str(k)
                            val = str(v)
                            setattr(result, key, val)
                    # print("result : ", result.__dict__)
                else:
                    # We need to get the result from the LUIS JSON which at every level returns an array.
                    to_entities = recognizer_result.entities.get("$instance", {}).get(
                        "To", []
                    )
                    if len(to_entities) > 0:
                        if recognizer_result.entities.get("To", [{"$instance": {}}])[0][
                            "$instance"
                        ]:
                            result.destination = to_entities[0]["text"].capitalize()
                        else:
                            result.unsupported_airports.append(
                                to_entities[0]["text"].capitalize()
                            )

                    from_entities = recognizer_result.entities.get("$instance", {}).get(
                        "From", []
                    )
                    if len(from_entities) > 0:
                        if recognizer_result.entities.get("From", [{"$instance": {}}])[0][
                            "$instance"
                        ]:
                            result.origin = from_entities[0]["text"].capitalize()
                        else:
                            result.unsupported_airports.append(
                                from_entities[0]["text"].capitalize()
                            )

                    orderid = recognizer_result.entities.get("$instance", {}).get(
                        "orderid", []
                    )
                    if len(orderid) > 0:
                        result.orderid = orderid[0]["text"]

        except Exception as exception:
            print(exception)
        # print("end execute_luis_query")
        return intent, result
