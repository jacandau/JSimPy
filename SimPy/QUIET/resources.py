'''
Created on 17 Sep 2015

@author: JCandau
'''

import simpy
import collections

def machine_store(env, machines, name):
    """ Create a machine store with a given name and list of machines to be included.
    This store has the usual get/put functionality.
    
    """
    store = simpy.Store(env, len(machines))
    store.items = machines
    store.name = name
    
    return store



class MyResource(object):
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
        
        yield self._resource.get()
        yield self.times_creation.popleft()
        
        
        
    def put(self, item):
        """ Add to the resource.
        """
        self._resource.items.append(item) # item has to be an event??
        self.times_creation.append(self.env.now)
        

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
    def __init__(self, env, name, resources = []):
        self.env = env
        self.name = name        
        self.resources = resources

        
    def get(self, part, number = 1):
        try:
            resource = [resource for resource in self.resources if resource.contained_class == part.__class__][0]
        except IndexError, e:
            raise Exception(e.message, 'The part requested does not exist in the Buffer %s' % (self.name))
        while range(number):
            yield resource.request()
        