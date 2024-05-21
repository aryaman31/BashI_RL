
from Environment.Actions.Action import Action
from Environment.State import State
from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor
from Environment.Games import GAME

class Environment:
    def __init__(self, controller: Controller, bashExtractor: BashExtractor):
        self.state = State("", "", 0)
        self.controller = controller
        self.bashExtractor = bashExtractor
        self.game = GAME.FIND_COMMAND
    
    def reset(self) -> State:
        initState = State("", "", 0)
        return initState
    
    def updateGame(self, cmd, err) -> GAME:
        print('Environment.updateGame NOT IMPLEMENTED')
        return GAME.FIND_COMMAND

    def step(self, action: Action) -> State:
        # get new payload
        newPayload = action.applyAction(self.state.previous_payload)

        # look for new input point if game is find_command
        if self.game == GAME.FIND_COMMAND:
            self.controller.findNewRequestPath()
        
        # send command
        self.bashExtractor.start()
        self.controller.makeRequest(newPayload)

        # see what bash command was actually run 
        cmd, err = self.bashExtractor.stop()

        # update game if necessary
        self.game = self.updateGame(cmd, err)

        # create new state from bash command returned + payload tested + error msg 
        self.state = State(cmd, newPayload, err)

        # return new state 
        return self.state
