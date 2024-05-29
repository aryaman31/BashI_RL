import random
import string

class Action:
    def __init__(self, actionTuple):
        self.actionId = actionTuple[0]
        self.arg1 = actionTuple[1]
        self.arg2 = actionTuple[2]
    
    def applyAction(self, payload):
        charToInsert = ''
        match self.actionId:
            case 0: 
                return self.__generateRandomString()
            case 1:
                options = ["&", ";", "||"]
                charToInsert = options[self.arg2]
            case 2:
                charToInsert = "#"
            case 3:
                options = ['(', ')']
                charToInsert = options[self.arg2]
            case 4:
                options = ['{', '}']
                charToInsert = options[self.arg2]
            case 5:
                options = ['[', ']']
                charToInsert = options[self.arg2]
            case 6:
                options = [':', '$']
                charToInsert = options[self.arg2]
            case 7:
                options = ['id', '/usr/bin/id', 'whoami', '/usr/bin/whoami', 'sleep 1']
                charToInsert = options[self.arg2]
        newPayload = list(payload)
        newPayload.insert(self.arg1, charToInsert)
        return "".join(newPayload)
    
    def getActionId(self):
        return self.actionId

    def __generateRandomString(self, length=10):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
