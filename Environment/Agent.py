import torch 
import torch.nn as nn
import torch.nn.functional as F
import random

from Environment.State import State
from Environment.Actions.Action import Action
from Environment.Games import GAME
from models.RL_Agent.DQN import DQN

# Needs to implement DQN properly with target and policy net. 
class Agent: 
    # Output needs to be of size 3 for action: (id, location, type)
    NETWORK = [4, 50, 50, 3] 

    def __init__(self):
        self.Q = DQN(State.size() + Action.size(), 1, "models/RL_Agent/", "DQN")
        self.game = GAME.CONTEXT_ESCAPE
        self.state = None
        self.clock = 0
    
    def updateGame(self, newState: State, identifier: str) -> GAME:
        executed = newState.executed_command.lower()
        error = newState.error_code
        reward = 0
        if error != 0:
            self.game = GAME.FIX_SYNTAX
            return self.game, -1
        
        if "sleep 0" in executed or 'echo -e “\x73\x6C\x65\x65\x70\x20\x30"' in executed:
            self.game, reward = GAME.FINISHED, 0
        elif self.__sanitised(newState):
            self.game, reward = GAME.SANITISATION_ESCAPE, -1
        elif self.__escapedContext(newState, identifier):
            self.game, reward = GAME.BEHAVIOR_CHANGE, -1
        else:
            self.game, reward = GAME.CONTEXT_ESCAPE, -1
        
        return self.game, reward

    def __escapedContext(self, state: State, identifier: str):
        executed = state.executed_command.lower().split(identifier)
        if len(executed) == 1:
            return False 
        
        prev = executed.strip().replace('${IFS}', '')
        return prev[-1] in Action.context_escape_tokens
    
    def __sanitised(self, state: State):
        executed = state.executed_command.lower()
        payload = state.previous_payload.lower()
        payload.replace('#', '')
        return payload not in executed

    def reset(self):
        self.clock = 0
        self.state = None 
        self.game = GAME.CONTEXT_ESCAPE

    def pickAction(self, state: State, explore=True):
        self.state = state
        self.clock += 1

        stateTensor = state.getStateTensor()
        availableActions = Action.getAvailableActions(self.game, state.previous_payload)

        bestQ = None 
        bestAction = None
        for potentialAction in availableActions:
            inp = torch.cat((stateTensor, potentialAction.getActionTensor()))
            currentQ = self.Q.get_Q_value(inp)[0][0]
            if not bestQ or bestQ < currentQ:
                bestQ = currentQ
                bestAction = potentialAction

        return bestAction
    
    def train(self, reward: int, newState: State):
        self.Q.cache(self.state.getStateTensor(), newState.getStateTensor(), reward)
        self.Q.tune_network(self.clock)

    def save(self, filename):
        torch.save(self.Q, filename)
    
    def load(self, filename):
        self.Q = torch.load(filename)