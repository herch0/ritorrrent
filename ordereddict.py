class OrderedDict:

    def __init__(self):
        self.keys = []
        self.values = []
        pass

    def add(self, key, value):
        self.keys.append(key)
        self.values.append(value)

    def remove(self, key):
        index
