'''
Created on 17 Sep 2015

@author: JCandau
'''

class Connections(object):
    """ This class contains the In - Out information in QUEST for each process.
    If two possible inputs or outputs are specified the priority is managed 
    by the BufferManager class.
    """
    
    _INIT_TOKEN = object()
    
    @classmethod
    def read_from_file(cls, file_name):
        #TODO
        pass
    
    @classmethod
    def read_from_list(cls, list_dict, elements):
        """ Start class from list_dict.
        
        Elements is an object containing all the elements created with a relation between their names and reference.
        
        :example:
        >>> list_dict = {'Str_ATL_2D': {'in': ['Stringer_Labour', 'Store_Layuptool_Stringer'],
                                         'out': ['Store_Layuptool_Stringer_Soiled', 'Freezer_Str_Forming_In']},
                          'Store_Layuptool_Stringer_Soiled': {'in': ['Str_ATL_2D'],
                                         'out': ['Stringer_Tool_Clean_Prep']},
                          'Stringer_Tool_Clean_Prep': {'in': ['Store_Layuptool_Stringer_Soiled', 'Store_Formtool_Stringer_Soiled'],
                                         'out': ['Store_Layuptool_Stringer']},
                          'Store_Layuptool_Stringer': {'in': 'Stringer_Tool_Clean_Prep'],
                                         'out': ['Str_ATL_2D']}}
        """

        connections = cls(list_dict, elements, cls._INIT_TOKEN)

        return connections
    
    def __init__(self, dictionary, elements, token = None):
        """ Creates instance with dictionary attribute.
        """
        if token is not self._INIT_TOKEN:
            raise ValueError("don't construct directly, use read_from_dictionary, read_from_file")
        self.dictionary = dictionary
        self._build()
        
    def _build(self):
        #TODO
        pass
    
    def build_process_connections(self, process):
        """ When connections.get(process) is called this method will return the input and output 
        objects for the process.
        
        :returns process instance: extra attributes
            process.in_labour = [labourResource1, labourResource2 ...]
            process.in_tool = [toolBuffer1, toolBuffer2 ...]
            process.in_parts = [partBuffer1, partBuffer2 ...]
            process.out_tool = [toolBuffer1, toolBuffer2 ...]
            process.out_parts = [partBuffer1, partBuffer2 ...]
            
        These will direct the input or output requests (get and put).
        """
        machine_name = process.machine.name
        connections_dictionary = self.dictionary[machine_name]
        # TODO: look through in and out list:
        #            * match with elements given name-->reference
        #            * get type of element: isStore() --> coming/going from/into machine
        #                                   isBuffer() -->coming/going from/into buffer
        return process
        