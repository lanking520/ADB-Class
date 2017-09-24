import re

class DataClean:
    def __init__(self, path):
        f = open(path)
        self.library = f.read().splitlines()

    def clean(self, query):
        # Half-piece
        query = re.sub('[^a-zA-Z0-9]', ' ', query)
        return query

    def stopWordRemoval(self, text):
        text = [w for w in text if not w in self.library and not w.replace('.', '', 1).isdigit()]
        return text