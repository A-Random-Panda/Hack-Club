'''Helping classes and functions for the mapmaker'''

import math
import logging
from scripts.editable_controls_FPC import FirstPersonController as _old_first_person_controller
from typing import override

_tolarance = 0.00001

#Declare logging
logger = logging.getLogger(__name__)

#Harry sucks so I have to do this
class FirstPersonController(_old_first_person_controller):
    '''
    Basically the update and physics update aren't in the same function
    so I need to do this
    '''
    @override
    def update(self):
        super().update()
        super().movement_not_in_cam()
        super().mouse_movement_not_in_cam()

def game_round(value:int|float, face) -> int:
    '''
    Rounding but it decides to round up or down depending on the face (1, 0, -1)
    '''
    logger.debug("Rounded %s with face value %s face equals 1 %s, face = -1 %s", value, face, face == 1.0, face == -1.0)
    if face == 1.0:
        logger.debug("Returned %s, face == 1", math.ceil(value))
        return math.ceil(value)
    if face == -1.0:
        logger.debug("Returned %s, face == -1", math.floor(value))
        return math.floor(value)
    logger.debug("Returned %s, face == rounded", math.copysign(math.floor(abs(value)+0.5),value)) #type: ignore
    return math.copysign(math.floor(abs(value) + 0.5), value) #type: ignore

def fuzzy_greater_than_equal(num1:int|float, num2:int|float) -> bool:
    '''
    Checks if they're greater then the other
    '''
    return num1 >= num2 + _tolarance
