'''
Created on 18 Sep 2015

@author: JCandau
'''
from QUIET.resources import machine_store, Buffer
import simpy
import collections
import unittest

from QUIET.log import Logger
import os
# Dummy classes for test

class Stringer(): pass
class Stringer1(): pass
class Tool(): pass


class TestResources(unittest.TestCase):
    
    ENV = simpy.Environment()
    st1 = Stringer(); st2 = Stringer(); st3 = Stringer(); st4 = Stringer()
    STRINGER_LIST = [st1, st2, st3]
    TIMES = collections.deque()
       
       
    def setUp(self):
        self.store = simpy.FilterStore(self.ENV)
        
    def _do_stuff(self):

        for stringer in self.STRINGER_LIST:
            yield self.ENV.timeout(1)
            self.store.put({"class":stringer.__class__, "time":self.ENV.now})
        
        self.len_times1 = len(self.store.items)
        
        part = yield self.store.get(lambda m: m["class"] == self.st4.__class__)
        part = yield self.store.get(lambda m: m["class"] == self.st4.__class__)
        part = yield self.store.get(lambda m: m["class"] == self.st4.__class__)
        part = yield self.store.get(lambda m: m["class"] == self.st4.__class__)
     
        yield self.ENV.timeout(1)

        self.store.put({"class":stringer.__class__, "time":self.ENV.now})
        
        
        
    def test_put(self):
        # Run simulation
        self.ENV.process(self._do_stuff())
        self.ENV.run(until=10)
        
        # Assert results
        self.assertEqual(len(self.STRINGER_LIST), self.len_times1)
        self.assertEqual([], self.store.items)
            
        with open('./log.txt', 'w') as o:
            o.writelines(Logger().get_monitor_list())
           

        
        
        
        
    