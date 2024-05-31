import random
import string
from itertools import product
import torch

from Environment.Games import GAME

class Action:
    def __init__(self, actionTuple):
        self.actionId = actionTuple[0]
        self.location = actionTuple[1]
    
    def applyAction(self, payload):
        newPayload = list(payload)

        if self.actionId <= 9:
            static = [';', '&&', '||', '&', '|', '#', Action.generateRandomString(letters=True), 
                 Action.generateRandomString(numbers=True), Action.generateRandomString(letters=True, numbers=True, punctuation=True), 
                 'sleep 0']
            charToInsert = static[self.actionId]
            newPayload.insert(self.location, charToInsert)
            return "".join(newPayload)


        match self.actionId:
            case 10:
                newPayload = self.__insertDouble(newPayload, '\'')
            case 11:
                newPayload = self.__insertDouble(newPayload, '\"')
            case 12:
                newPayload = self.__insertDouble(newPayload, '`')
            case 13:
                s = ''.join(newPayload)
                newPayload = list(s.replace(" ", "${IFS}"))
            case 14: 
                # Should do this for any combination of caps in 'sleep 0'
                s = ''.join(newPayload)
                newPayload = list(s.replace("sleep 0", ' echo -e “\x73\x6C\x65\x65\x70\x20\x30"'))
            case 15: 
                # Should do this for any combination of caps in 'sleep 0'
                s = ''.join(newPayload)
                newPayload = list(s.replace("/", '${HOME:0:1}'))
            # Add a random slashes before chars
    
    def getActionTensor(self):
        return torch.tensor([self.actionId, self.location])
    
    def getAvailableActions(game, payload):
        n = len(payload)
        injLocs = list(range(0, n))
        match game:
            case GAME.CONTEXT_ESCAPE:
                validActions = list(range(0, 8 + 1))
            case GAME.BEHAVIOR_CHANGE:
                validActions = [9]
            case GAME.SANITISATION_ESCAPE:
                validActions = list(range(10, 16 + 1))
            case _ : 
                return []
        
        return [Action(a, l) for a, l in product(validActions, injLocs)]


    def getActionId(self):
        return self.actionId

    def __insertDouble(self, payload, char, dist=2):
        payload.insert(self.location, char)
        payload.insert(self.location + dist, char)
        return payload

    def generateRandomString(length=10, letters=False, numbers=False, punctuation=False):
        characters = ''
        if letters: characters += string.ascii_letters
        if numbers: characters += string.digits
        if punctuation: characters += string.punctuation 

        assert(len(characters) > 0)
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
