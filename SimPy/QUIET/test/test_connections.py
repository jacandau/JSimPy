'''
Created on 17 Sep 2015

@author: JCandau
'''
from QUIET.connections import Connections
import unittest

class TestConnections(unittest.TestCase):
    
    DICTIONARY1 = None
    ELEMENTS1 = None
    PROCESS = None
    
    def setUp(self):
        self.connections1 = Connections.read_from_list(self.DICTIONARY1, self.ELEMENTS1)
    
    def test_build_process_connections(self):
        self.connections1.build_process_connections(self.PROCESS)