
class ResponseHolder(object):

    def __init__(self):
        self.responses = dict()

    def add(self, id, response):
        if id in self.responses:
            raise Exception("Id Not Unique")
        else:
            self.responses[id] = response
