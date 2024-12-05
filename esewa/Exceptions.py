class InvalidSyntaxError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidSignatureError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PaymentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RefundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)