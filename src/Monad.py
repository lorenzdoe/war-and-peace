class Maybe:
    def __init__(self, value=None, is_error=False):
        self.value = value
        self.is_error = is_error

    def bind(self, func):
        if self.is_error:
            return self
        try:
            return Maybe(func(self.value))
        except Exception as e:
            return Maybe(None, is_error=True)

    def __str__(self):
        if self.is_error:
            return "Error"
        return f"Value: {self.value}"