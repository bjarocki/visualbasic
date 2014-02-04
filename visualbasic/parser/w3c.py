import re

class W3CParser(class):

    def __init__(self):
        self.regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) - "(.*?)" "(.*?)"'

    def parse(self, data):
        try:
            return re.match(self.regex, data).groups()
        except:
            return []
