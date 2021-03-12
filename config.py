#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    # APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_ID = "c8f37f28-fe29-4cea-8470-525c2f05239e"
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_PASSWORD = "AtLeastSixteenCharacters_0"
    # LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_APP_ID = "f4d98386-e756-45b5-adce-8cc986753e56"
    # LUIS_APP_ID = "61a7ba18-902e-4b9c-be95-dc27dbd549a4"
    # LUIS_API_KEY = "f72af9e36f094c08a9725d088c7bbfc2"
    LUIS_API_KEY = "ccb5f5a33255424096422b9d212908be"
    # LUIS_API_KEY = "0607928ef0d64657aa37e7cb45b83b5d"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    # LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    LUIS_API_HOST_NAME = "westus.api.cognitive.microsoft.com"
