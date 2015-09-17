'''
Stringer Manufacture

Scenario:
    The first part in the manufacture of a composite wing is the stringer production.
    
'''

import simpy
import contextlib

from log import Logger
import itertools
from collections import OrderedDict



RANDOM_SEED = 42
SIM_TIME = 1000           # Simulation time in hours
NUM_STRINGERS = 11
LAYUP_TIMES = [7.62, 22.59, 26.82, 40.91, 55.00, 60.90, 52.13, 45.79, 32.92, 22.04, 10.12]
CLEAN_AND_PREP_TIMES = [.00, .00, .00, .00, .00, .00, .00, .00, .00, .00, .00]
INITIAL_TOOL_STOCK = [20 for k in CLEAN_AND_PREP_TIMES]
NUM_MACHINES = 9
NUM_CLEANERS = 3
STRINGER_DELAY = 80
BATCH_SIZE = 8

# Components to lay up (in ordered lists)
types = ['Stringer']    # ['Stringer', 'Spar']
sides = ['top']         # ['top', 'bot']
numbers = [k for k in range(NUM_STRINGERS)]


# Process logic from inputs
process_logic = OrderedDict({'Stringer':{}})

used_tools = []

class ComponentCreator(object):
    """ Factory to generate components.
    """
    def __init__(self, env, store, component, *args):
        self.stringer_generator = itertools.cycle(itertools.product(*args))
        self.env = env
        self.store = store
        self.component_class = component
        
    def create_component(self,  num = 1):
        """ Create the amount of stringers specified in num (default 1) by looping 
        around the cyclical generator.
        """
        for x in range(num):
            
            stringer = self.stringer_generator.next()

            component = self.component_class(stringer[0], stringer[1], stringer[2], self, BATCH_SIZE)
            Logger().add_event('%s %s created and added to store %s queue at time %s\n' % (component.__class__, component.name, self.store.name, self.env.now))
            self.env.process(component.layup(self.env, self.store))


#TODO: define stringer queue creation. See example below
class Component(object):
    
    class_instances = []
    
    def __init__(self, part_type, side, number, component_creator, quantity = 1):
        """
        This class represents the stringer or spar that will be generated in the ATL machines.
        
        :params part_type: 'Stringer' or 'Spar'
        :params side: 'top' or 'bot'
        :params number(int): Number of the stringer
        """
        self.part_type = part_type
        self.side = side
        self.number = number
        self.quantity = quantity # when it's a batch
        self.name = "%s_%s_%s_batch_of_%s" % (self.part_type, self.side, self.number, BATCH_SIZE)
        self.component_creator = component_creator
        self.__class__.class_instances.append(self)
        
    def get_cycle_time(self):
        """ Get cycle time from the UI inputs.
        """
        # TODO
        return LAYUP_TIMES[self.number]
        
    def get_tool_resource(self):
        # TODO: return resource tool with 2D ATL props
        return None
    
    def get_labour_resource(self):
        # TODO: return resource labour with 2D ATL props
        return None
    
    def get_products(self):
        # TODO: return products for each process (parts and soiled tools). Think of an input structure from QUIET data to do this automatically
        parts = Component()
    
    def layup(self, env, machine_store):
        """ The component (has a *name*) arrives at the machine and requests
        the tools and labour.
        
        It then starts the layup process, finishes, changes its status and
        moves to the buffer (Resource) as a finished part.
        """
        
        # Request machine to store
        machine = yield machine_store.get()
        
        # Request tools and labour
        #with self.get_tool_resource().request() as req_tool,self.get_labour_resource().request() as req_labour: 
            
            #yield req_tool & req_labour
        
        # send to the machine for work    
        Logger().add_event('ATLComponent %s gets tools, labour and machine %s at time %s\n' % (self.name, machine, env.now))
        yield env.process(machine.working(self))
        
        # add new element to queue
        self.component_creator.create_component()
        
        # send to buffer or next process
        yield env.process(buffer_handler.put(products))
        
class Machine(object):
    """ Machine that lays the stringer laminates.
    
    Responsible to get the next stringer in a queue and work on it.
    """
    class_instances = []
    
    def __init__(self, env, name, resource):
        """A machine produces parts with the usage of a tool and labor.

        A machine has a *name* and a number of *parts_made* thus far.
        It also uses the composition principle to relate to a Resource that simulates the amount
        and availability of machines.
    
        """

        self.env = env
        self.name = name
        self.parts_made = 0
        self.prepared = False
        self._resource = resource
        self.__class__.class_instances.append(self)
            
    def working(self, part):
        """ Produce parts as long as the simulation runs.
        
        *work_to_do* is the list of processes to be done in the machine.
        *component_creator* is the creator of components to the queue (pull system is implemented)
        """
        

        # Prepare the machine for the next batch
        yield self.env.process(self._prepare())
        
        # get the part to be processed
        yield self.env.timeout(part.get_cycle_time())
            
        # Part is done
        self.parts_made += 1
        Logger().add_event('Created part %s in machine %s at time %s\n' % (part.name, self.name, self.env.now))

        # Return the machine to the store
        yield machine_store.put(self)
   
    def _prepare(self):
        
        Logger().add_event('Preparing machine %s (will take time %s) at time %s\n' % (self.name, STRINGER_DELAY, self.env.now))
        
        yield self.env.timeout(STRINGER_DELAY)

class BufferHandler(object):
    """ This class contains the structure of Stores and Resources to contain all the semi-products
    and tools (new or used) in the system.
    
    It is responsible for storing and requesting parts and tools from the different buffers.
    """
    def __init__(self,  stores = []):
        self.stores = stores
    
    def get(self, *args):
        """ Get the parts and tools contained in *args from the stores.
        """
        pass
        # Identify store and resource for each
        
        # Request sequentially (logic is that everything is needed and independent so the order won't affect).

# Create elements in the model
env = simpy.Environment()
machine_resource = simpy.Resource(env, capacity = NUM_MACHINES)
machines = [Machine(env, 'Str_ATL_2D_%s' % (k), machine_resource) for k in range(NUM_MACHINES)]
machine_store = simpy.Store(env, len(machines))
machine_store.items = machines
machine_store.name = 'Str_ATL_2D_store'
component_creator = ComponentCreator(env, machine_store, Component, types, sides, numbers)


# Create buffers (process to be automated)

buffer_handler = BufferHandler()


# Requests first stringers before simulation starts
for stringer in range(NUM_MACHINES+2):
    component_creator.create_component()



#try:
env.run(until = SIM_TIME)
#except: pass
with open('./log', 'w') as o:
    o.writelines(Logger().get_monitor_list())

for machine in Machine.class_instances:    
    print machine.name, machine.parts_made 
# old code   
'''class MachineController(object):
    """ Class that manages the request for machine.
    """
    def __init__(self, machine_list):
        self.machine_list = machine_list
        
    def request(self):
        machine = self.machine_list[0]
        with machine.request() as req:# for machine in self.machine_list
            yield req   # | ... reqn'''