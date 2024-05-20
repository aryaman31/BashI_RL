from enum import Enum 

class GAME(Enum):
    FIND_COMMAND = 1
    CONTEXT_ESCAPE = 2
    BEHAVIOR_CHANGE = 3
    SANITISATION_ESCAPE = 4
    FIX_SYNTAX = 5

    def __str__(self) -> str:
        return self._name_
    
    def __repr__(self) -> str:
        return self.__str__()