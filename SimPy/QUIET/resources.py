'''
Created on 17 Sep 2015

@author: JCandau
'''

import simpy
import collections
from log import Logger
from simpy.events import Event

def machine_store(env, machines, name):
    """ Create a machine store with a given name and list of machines to be included.
    This store has the usual get/put functionality.
    
    """
    store = simpy.Store(env, len(machines))
    store.items = machines
    store.name = name
    
    return store

'''# Filter Store
def user(machine):
    m = yield machine.get()
    print(m)
    yield machine.put(m)

    m = yield machine.get(lambda m: m['id'] == 1)
    print(m)
    yield machine.put(m)

    m = yield machine.get(lambda m: m['health'] > 98)
    print(m)
    yield machine.put(m)


env = simpy.Environment()
machine = simpy.FilterStore(env, 3)
machine.put({'id': 0, 'health': 100})
machine.put({'id': 1, 'health': 95})
machine.put({'id': 2, 'health': 97.2})

env.process(user(machine))

env.run()'''

'''class MyResource(object):
    """ Customised resource extending the simpy.resource behaviour.
     
    """
    def __init__(self, env, contained_part):
        """"""
        self.env = env
        self._resource = simpy.Store(self.env)
        # take the one bit of capacity away
        self.contained_class = contained_part
        self.times_creation = collections.deque()
            
    def get(self):
        """ Request from the resource.
        """
        
        resource = yield self._resource.get()
        Logger().add_event('Contained resource %s released at time %s\n' % (resource, self.env.now))
        self.times_creation.popleft()        
        
        
    def put(self, item):
        """ Add to the resource.
        """
        
        self._resource.items.append(item) # item has to be an event??
        self.times_creation.append(self.env.now)
        Logger().add_event('Added resource %s at time %s\n' % (item, self.env.now))'''
        

class Buffer(object):
    """ The most generic buffer can contain different types of parts 'str_top_1', ...,'str_top_11'.
    It needs to know what it contains to only put that and get that.
    It is composed by one resource for each item it contains.
    Needs to aid for BufferManager logic. FIFO, LIFO, ...
    
    methods can contain:
     - get(name, number = 1)
     - get_all(number,  number = 1)
     - put(name, number = 1)
     - get_any(number = 1) # FIFO
     - get_newest(number = 1) # LIFO
    """
    def __init__(self, env, name, store):
        self.env = env
        self.name = name        
        self.store = store

        
    def get(self, part):
        my_class = part.__class__
        part = yield self.store.get(lambda m: m['class'] == my_class)
        
    
        