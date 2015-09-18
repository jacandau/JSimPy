'''
Created on 18 Sep 2015

@author: JCandau
'''
from QUIET.resources import machine_store, MyResource, Buffer
import simpy
import collections
import unittest

# Dummy classes for test

class Stringer(): pass
class Stringer1(): pass
class Tool(): pass


class TestResources(unittest.TestCase):
    
    ENV = simpy.Environment()
    st1 = Stringer(); st2 = Stringer(); st3 = Stringer()
    STRINGER_LIST = [st1, st2, st3]
    TIMES = [1,2,3]
          
    def setUp(self):
        self.myResource = MyResource(self.ENV, Stringer)
        
    def _do_stuff(self):

        for stringer in self.STRINGER_LIST:
            yield self.ENV.timeout(1)
            self.myResource.put(stringer)
        
        self.len_times1 = len(self.myResource._resource.items)
        
        part = self.ENV.process(self.myResource.get())

        print type(part)


        
        
    def test_put(self):
        # Run simulation
        self.ENV.process(self._do_stuff())
        self.ENV.run(until=10)
        
        # Assert results
        self.assertEqual(len(self.STRINGER_LIST), self.len_times1)
        self.assertEqual(self.TIMES, self.myResource.times_creation)
            
        
            

        
        
        
        
    