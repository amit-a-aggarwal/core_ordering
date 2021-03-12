# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class OrderingDetails:
    def __init__(
        self,
        email: str = None,
        orderid: str = None,
    ):
        self.email = email
        self.orderid = orderid

