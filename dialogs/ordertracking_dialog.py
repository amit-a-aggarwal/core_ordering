# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from helpers.luis_helper import LuisHelper, Intent
from ordering_recognizer import OrderingRecognizer
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog
import json

class OrderTrackingDialog(CancelAndHelpDialog):
    def __init__(self,luis_recognizer: OrderingRecognizer,dialog_id: str = None):
        super(OrderTrackingDialog, self).__init__(dialog_id or OrderTrackingDialog.__name__)
        self._luis_recognizer = luis_recognizer
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.email_step,
                    self.orderid_step,
                    self.final_step,
                ],
            )
        )
        self.initial_dialog_id = WaterfallDialog.__name__

    async def email_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        ordering_details = step_context.options
        if ordering_details.email is None:
            message_text = "Please enter your email id."
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(ordering_details.email)

    async def orderid_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        ordering_details = step_context.options

        # Capture the response to the previous step's prompt
        ordering_details.email = step_context.result
        if ordering_details.orderid is None:
            message_text = "Please enter your order id."
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        # return await step_context.next(ordering_details.orderid)
        user_input = ""
        return await step_context.next(user_input)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        ordering_details = step_context.options
        # ordering_details.orderid = step_context.result
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        msg_txt = "Your order has arrived at chicago and will be delivered in 2 days."
        dict = {}
        dict["input"] = step_context.context.activity.text
        dict["text"] = msg_txt
        dict["intent"] = intent
        ents = {}
        for i in luis_result.__dict__.keys():
            if luis_result.__dict__[i] != None:
                ents[i] = luis_result.__dict__[i]
                setattr(ordering_details, i, luis_result.__dict__[i])
        dict["entities"] = ents
        dict["context"] = step_context.options.__dict__
        txt = json.dumps(dict)
        return await step_context.end_dialog(txt)


    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
