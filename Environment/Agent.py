import torch 
import torch.nn as nn
import torch.nn.functional as F
import random

from Environment.State import State
from Environment.Actions.Action import Action
from Environment.Games import GAME

# Needs to implement DQN properly with target and policy net. 
class Agent: 
    # Output needs to be of size 3 for action: (id, location, type)
    NETWORK = [4, 50, 50, 3] 

    def __init__(self):
        self.Q = DQN(Agent.NETWORK)
        self.game = GAME.FIND_COMMAND
    
    def updateGame(self, state: State) -> GAME:
        print("Agent.updateGame NOT IMPLEMENTED YET")
        executed = state.executed_command.lower()
        error = state.error_code
        if error != 0:
            return GAME.FIX_SYNTAX
        
        if "sleep 0" in executed or 'echo -e “\x73\x6C\x65\x65\x70\x20\x30"' in executed:
            return GAME.FINISHED
        elif self.__sanitised(state):
            return GAME.SANITISATION_ESCAPE
        elif self.__escapedContext(state):
            return GAME.BEHAVIOR_CHANGE
        else:
            return GAME.CONTEXT_ESCAPE
        
        return GAME.FIND_COMMAND

    def __escapedContext(self, state: State):
        print("Agent.__escapedContext NOT IMPLEMENTED YET")
        return True
    
    def __sanitised(self, state: State):
        executed = state.executed_command.lower()
        payload = state.previous_payload.lower()
        payload.replace('#', '')
        return payload in executed

    def pickAction(self, state: State, explore=True):
        stateTensor = state.getStateTensor()

        # update game accordingly here
        self.game = self.updateGame(state)

        availableActions = Action.getAvailableActions(self.game, state.previous_payload)

        bestQ = None 
        bestAction = None
        for potentialAction in availableActions:
            inp = torch.cat(stateTensor, potentialAction.getActionTensor())
            currentQ = self.Q(inp)
            if bestQ and bestQ < currentQ:
                bestQ = currentQ
                bestAction = potentialAction

        return bestAction

    def save(self, filename):
        torch.save(self.Q, filename)
    
    def load(self, filename):
        self.Q = torch.load(filename)

class DQN(nn.Module):
    def __init__(self, layer_sizes:list[int]):
        super(DQN, self).__init__()
        self.layers = nn.ModuleList([nn.Linear(layer_sizes[i], layer_sizes[i+1]) for i in range(len(layer_sizes)-1)])
    
    def forward (self, x:torch.Tensor)->torch.Tensor:
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        x = self.layers[-1](x)
        return x
