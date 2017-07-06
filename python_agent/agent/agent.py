from response_holder import ResponseHolder
# from import_hooks import *

class Agent(object):
    def __init__(self):
        def counting(fn):
            def wrapper(*args, **kwargs):
                wrapper.called += 1
                return fn(*args, **kwargs)

            wrapper.called = 0
            wrapper.__name__ = fn.__name__
            return wrapper

        global str
        str = counting(str)
        str.__init__ = counting(str.__init__)
        str.__new__ = counting(str.__new__)
        self.response_holder = ResponseHolder()
        self.file = open("times.txt", "wb")
        self.memory_logger = open('memory_profiler.log', 'w+')


global agent
agent = Agent()
