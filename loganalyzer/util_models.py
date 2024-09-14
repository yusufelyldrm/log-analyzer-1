
class Log:
    def __init__(self, date_string, text):
        self.date_string = date_string
        self.text = text

    def __repr__(self):
        return f"{self.date_string} {self.text}"