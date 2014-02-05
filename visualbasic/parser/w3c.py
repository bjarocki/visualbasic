import re

class Parser(object):

    def __init__(self):
        self.regex = '(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?)\] "(?P<method>.*?) (?P<uri>.*?) (?P<httpv>.*?)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>.*?)" "(?P<agent>.*?)"'

    def __parse(self, data):
        try:
            return re.match(self.regex, data)
        except:
            return []

    def get_key(self, data, key):
        try:
            return self.__parse(data).group(key)
        except:
            return []
