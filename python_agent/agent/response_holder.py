import json


class ResponseHolder(object):

    def __init__(self):
        self.responses = dict()

    def add(self, id, response):
        if id in self.responses:
            raise Exception("Id Not Unique")
        else:
            self.save(id, response)
            self.responses[id] = response

    def save(self, id, response):
        with open('data.txt', 'a') as outfile:
            json.dump({id: response}, outfile)
