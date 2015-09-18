'''
Created on 17 Sep 2015

@author: JCandau
'''

class Buffer(object):
    """ The most generic buffer can contain different types of parts 'str_top_1', ...,'str_top_11'.
    It needs to know what it contains to only put that and get that.
    It is composed by one resource for each item it contains.
    Needs to aid for BufferManager logic. FIFO, LIFO, ...
    
    methods can contain:
     - get(name, number = 1)
     - get(one_of_each, number = 1)
     - put(name, number = 1)
     - get_any(number = 1) # FIFO
     - get_newest(number = 1) # LIFO
    """
    def __init__(self, env, store = ):