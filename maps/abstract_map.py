'''Module that contains the abstract map class'''
import abc

class AbstractMap(abc.ABC):
    '''Abstract map class'''

    @classmethod
    @abc.abstractmethod
    def load_map(cls):
        '''Function to load map'''
        pass

    @classmethod
    @abc.abstractmethod
    def unload_map(cls):
        '''Function to unload map'''
        pass

    @classmethod
    @abc.abstractmethod
    def update(cls):
        '''
        The objects in the map that needs to be updated every frame
        Meant to be put into the update handler.        
        '''
        pass
