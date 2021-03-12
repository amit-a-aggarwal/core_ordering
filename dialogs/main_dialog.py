# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints

from ordering_details import OrderingDetails
from ordering_recognizer import OrderingRecognizer
from helpers.luis_helper import LuisHelper, Intent

from .ordertracking_dialog import OrderTrackingDialog
from .orderstatus_dialog import OrderStatusDialog
# import json

class MainDialog(ComponentDialog):
    def __init__(
            self, luis_recognizer: OrderingRecognizer, orderstatus_dialog: OrderStatusDialog,
            ordertracking_dialog: OrderTrackingDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._orderstatus_dialog_id = orderstatus_dialog.id
        self._ordertracking_dialog_id = ordertracking_dialog.id
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(orderstatus_dialog)
        self.add_dialog(ordertracking_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )
        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )
            return await step_context.next(None)
        # print("step_context.options : ", str(step_context.options))
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
        # return await step_context.next(InputHints.expecting_input)

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            # return await step_context.begin_dialog(
            #     self._orderstatus_dialog_id, BookingDetails()
            # )
            return await step_context.begin_dialog(
                self._orderstatus_dialog_id, OrderingDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.ORDER_STATUS.value and luis_result:
            # Run the OrderStatusDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._orderstatus_dialog_id, luis_result)

        if intent == Intent.ORDER_TRACKING.value and luis_result:
            # Run the OrderTrackingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._ordertracking_dialog_id, luis_result)

        if intent == Intent.GET_WEATHER.value:
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if step_context.result is not None:
            msg_txt = step_context.result
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        else:
            msg_txt = "Something went wrong."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)
