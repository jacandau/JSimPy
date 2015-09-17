'''
Created on 16 Sep 2015

@author: JCandau
'''

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(object):
    __metaclass__ = Singleton
    def __init__(self):
        self._monitor_list = []
    def get_monitor_list(self):
        return self._monitor_list
    def add_event(self, event):
        self._monitor_list.append(event)
        
if __name__ == '__main__':
    log = Logger()
    log.add_event('hello')
    log2 = Logger()
    log2.add_event('world!')
    print Logger().get_monitor_list() # prints ['hello', 'world!']