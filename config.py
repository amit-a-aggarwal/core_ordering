#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    # APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_ID = "b5e3cf0f-d88c-4688-9fb4-6cce12985cf3"
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_PASSWORD = "AtLeastSixteenCharacters_0"
    # LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_APP_ID = "107db1f0-718b-4e72-a642-436657e7d7c9"
    # LUIS_APP_ID = "61a7ba18-902e-4b9c-be95-dc27dbd549a4"
    # LUIS_API_KEY = "f72af9e36f094c08a9725d088c7bbfc2"
    LUIS_API_KEY = "55d7c0f70556494c9b5d6fd1908794bd"
    # LUIS_API_KEY = "0607928ef0d64657aa37e7cb45b83b5d"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    # LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    LUIS_API_HOST_NAME = "westus.api.cognitive.microsoft.com"
