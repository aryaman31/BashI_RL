from Environment.State import State
from Environment.Actions.Action import Action
from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor

class BashI_Environment:
    def __init__(self, controller: Controller, bashExtractor: BashExtractor):
        self.state = State("", "", 0)
        self.controller = controller
        self.bashExtractor = bashExtractor
        self.cmd = ''
    
    def findNextTarget(self):
        uniqueId = Action.generateRandomString(letters=True, numbers=True)
        found = True 
        while found:
            inpFound = self.controller.findNewRequestPath()
            if not inpFound: return False
            self.bashExtractor.start()
            self.controller.makeRequest(uniqueId)
            cmd, err = self.bashExtractor.stop(uniqueId)
            found = len(cmd) > 0
        return True
    
    def reset(self) -> State:
        initState = State("", "", 0)
        return initState

    def step(self, action: Action) -> State:
        # get new payload
        newPayload = action.applyAction(self.state.previous_payload)
        
        # send command
        self.bashExtractor.start()
        self.controller.makeRequest(newPayload)

        # see what bash command was actually run 
        cmd, err = self.bashExtractor.stop(newPayload)
        if err == 0:
            self.cmd = cmd

        # create new state from bash command returned + payload tested + error msg 
        self.state = State(self.cmd, newPayload, err)

        # return new state 
        return self.state

    
if __name__ == '__main__':
    controller = Controller("http://localhost:8000/")
    bashExtractor = BashExtractor(16956) # have to manually get this :( 
    env = BashI_Environment(controller, bashExtractor)

    initState = env.reset()

    dummyAction = Action((0, 0, 0)) # For state find command 
    newState = env.step(dummyAction)
    print(newState)

