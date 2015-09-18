"""
Machine shop example

Covers:

- Interrupts
- Resources: PreemptiveResource

Scenario:
  A workshop has *n* identical machines. A stream of jobs (enough to
  keep the machines busy) arrives. Each machine breaks down
  periodically. Repairs are carried out by one repairman. The repairman
  has other, less important tasks to perform, too. Broken machines
  preempt theses tasks. The repairman continues them when he is done
  with the machine repair. The workshop works continuously.

"""
import random

import simpy
import numpy as np
from monitoring import patch_resource, monitor
from _functools import partial
import datetime


RANDOM_SEED = 42       # integer to select starting value for random functions
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 30.0     # Time it takes to repair a machine in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_MACHINES = 10      # Number of machines in the machine shop
WEEKS = 4            # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes
BROKEN_MACHINES = []
 # Storing cycle times created by Python random to match with Quest


def time_per_part():
    """Return actual processing time for a concrete part."""
    time = random.normalvariate(PT_MEAN, PT_SIGMA)
    return time

def time_to_failure():
    """Return time until next failure for a machine."""
    return random.expovariate(BREAK_MEAN)


class Machine(object):
    """A machine produces parts and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A machine has a *name* and a numberof *parts_made* thus far.

    """
    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False

        # Start "working" and "break_machine" processes for this machine.
        self.process = env.process(self.working(repairman))
        env.process(self.break_machine())
        
        self.PT_CREATED_POINTS = []
        self.TIMES_TO_FAILURE = []
        self.prev_time_creation = 0
        self.prev_time = 0
        self.last_fixed_time = 0
    def working(self, repairman):
        """Produce parts as long as the simulation runs.

        While making a part, the machine may break multiple times.
        Request a repairman when this happens.

        """
        while True:
            # Start making a new part
            done_in = time_per_part()
            self.PT_CREATED_POINTS.append(self.prev_time_creation + done_in*60)
            #self.prev_time_creation = self.PT_CREATED_POINTS[-1]
            while done_in:
                try:
                    # Working on the part
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0  # Set to 0 to exit while loop.

                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start  # How much time left?

                    # Request a repairman. This will preempt its "other_job".
                    with repairman.request(priority=1) as req:
                        #req.machine = self.name
                        yield req
                        print 'starting repair at time %d:%.0f to %s' % (env.now, (env.now%1)*60, self.name)
                        self.last_fixed_time = env.now + 30
                        BROKEN_MACHINES.remove(self.name)
                        print 'Broken machines'+ BROKEN_MACHINES.__repr__()
                        yield self.env.timeout(REPAIR_TIME)


                    self.broken = False

            # Part is done.
            self.parts_made += 1

    def break_machine(self):
        """Break the machine every now and then."""
        
        while True:
            ttf = time_to_failure()
            #print 'Next failure scheduled for %s in %d:%.0f' % (self.name, ttf, (ttf%1)*60)
            
            #self.prev_time = self.TIMES_TO_FAILURE[-1]
            yield self.env.timeout(ttf)
            if not self.broken:
                # Only break the machine if it is currently working.
                BROKEN_MACHINES.append(self.name)
                print "Broken %s at time %d:%.0f" % (self.name, env.now, (env.now%1)*60)
                self.TIMES_TO_FAILURE.append(self.env.now * 60 - self.last_fixed_time * 60)
                self.process.interrupt()


def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = JOB_DURATION
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman.request(priority=2, preempt = False) as req:
                #req.machine = "Idle Time"
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start


# Setup and start the simulation
print('Machine shop')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()





repairman = simpy.PreemptiveResource(env, capacity=1)
# Trace repairman
data = []
monitor = partial(monitor, data)
patch_resource(repairman, post=monitor)




machines = [Machine(env, 'Machine %d' % (i + 1), repairman)
        for i in range(NUM_MACHINES)]
env.process(other_jobs(env, repairman))

# Execute!
env.run(until=SIM_TIME)


def make_relative(list_of_absolute_times, delay = 0):
    if len(list_of_absolute_times)>1:
        list_rel_times = []
        while len(list_of_absolute_times)>1:
            list_rel_times.insert(0, list_of_absolute_times.pop()- list_of_absolute_times[-1] - delay)
        list_rel_times.insert(0, list_of_absolute_times.pop())
        return list_rel_times
    else: 
        return list_of_absolute_times
    
# Analyis/results
print('Machine shop results after %s weeks' % WEEKS)
for machine in machines:
    print('%s made %d parts.' % (machine.name, machine.parts_made))
    machine_number = machines.index(machine) + 1
    np.savetxt("failure_times%s.csv" % machine_number, machine.TIMES_TO_FAILURE, delimiter = ",", newline = "\n")
    np.savetxt("times_per_part%s.csv" % machine_number, machine.PT_CREATED_POINTS, delimiter = ",", newline = "\n")

print data
# TODO: Print some kind of report