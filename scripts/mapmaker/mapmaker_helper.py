'''Helping classes and functions for the mapmaker'''

import math
import logging
from scripts.editable_controls_FPC import FirstPersonController as fpc
from typing import override

_tolarance = 0.00001

#Declare logging
logger = logging.getLogger(__name__)

#Harry sucks so I have to do this
class FirstPersonController(fpc):
    '''
    Basically the update and physics update aren't in the same function
    so I need to do this
    '''
    @override
    def update(self):
        super().update()
        super().movement_not_in_cam()

def game_round(value:int|float, face) -> int:
    '''
    Rounding but it decides to round up or down depending on the face (1, 0, -1)
    '''
    logger.debug("Rounded %s with face value %s", value, face)
    if fuzzy_greater_than_equal((value - math.floor(value)), .5):
        if face == 1.0:
            logger.debug("Returned %s", math.ceil(value))
            return math.ceil(value)
        if face == -1.0:
            logger.debug("Returned %s", math.floor(value))
            return math.floor(value)
    logger.debug("Returned %s", math.copysign(math.floor(abs(value)+0.5),value)) #type: ignore
    return math.copysign(math.floor(abs(value) + 0.5), value) #type: ignore

def fuzzy_greater_than_equal(num1:int|float, num2:int|float) -> bool:
    '''
    Checks if they're greater then the other
    '''
    return num1 >= num2 + _tolarance
