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
    counter = 0
    def __init__(self):
        self.Q = DQN(State.size() + Action.size(), 1, "models/RL_Agent/", "DQN")
        self.game = GAME.CONTEXT_ESCAPE
        self.state = None # This is the state the pick action was called on
        self.chosenAction = None
        self.tensor_history = []
        self.reward_history = []
        self.epsilon = 0.4
    
    def updateGame(self, newState: State, before: str, after: str) -> GAME:
        executed = newState.executed_command.lower()
        error = newState.error_code
        executed_payload = executed.split(before)[-1].split(after)[0]
        reward = 0
        if error != 0:
            # self.game = GAME.FIX_SYNTAX
            # return self.game, -1
            reward = -1
        
        if error == 0 and ("sleep 0" in executed or 'echo -e “\x73\x6C\x65\x65\x70\x20\x30"' in executed):
            self.game, reward = GAME.FINISHED, 0
        elif self.__sanitised(newState):
            self.game = GAME.SANITISATION_ESCAPE
            reward += -1
        elif self.__escapedContext(before, after, executed_payload, executed):
            self.game = GAME.BEHAVIOR_CHANGE
            reward += -1
        else:
            self.game = GAME.CONTEXT_ESCAPE
            reward += -1
        
        return self.game, reward

    def __escapedContext(self, before: str, after: str, executed_payload: str, executed_command: str):
        matches = 0
        matches += executed_command.startswith(before)
        matches += (executed_command.endswith(after) and len(after) > 0)
        return sum([c in executed_payload for c in Action.context_escape_tokens]) == matches
    
    def __sanitised(self, state: State):
        executed = state.executed_command.lower()
        payload = state.previous_payload.lower().split('#', 1)[0]
        return payload not in executed

    def reset(self):
        self.state = None 
        self.game = GAME.CONTEXT_ESCAPE

    def pickAction(self, state: State, explore=True):
        self.state = state
        Agent.counter += 1

        stateTensor = state.getStateTensor()
        availableActions = Action.getAvailableActions(self.game, state.previous_payload, state.error_code)

        if not explore:
            return self.__greedyAction(availableActions, stateTensor)

        return self.__epsilonGreedyAction(availableActions, stateTensor)

    def __greedyAction(self, availableActions, stateTensor):
        bestQ = None 
        bestAction = None
        bestInp = None
        for potentialAction in availableActions:
            inp = torch.cat((stateTensor, potentialAction.getActionTensor()))
            currentQ = self.Q.get_Q_value(inp)[0][0]
            if not bestQ or bestQ < currentQ:
                bestQ = currentQ
                bestAction = potentialAction
                bestInp = inp

        self.tensor_history.append((bestInp, torch.tensor(bestQ)))
        return bestAction
    
    def __epsilonGreedyAction(self, availableActions, stateTensor):
        greedy = self.__greedyAction(availableActions, stateTensor)
        p = float(torch.rand(1))
        if p > self.epsilon:
            return greedy
        else:
            return random.choice(availableActions)

    
    def train(self, reward: int):
        self.reward_history.append(reward)
        s, q = self.tensor_history[-1]
        if len(self.tensor_history) >= 2:
            self.Q.cache(s, q, self.reward_history[-2])
        self.Q.tune_network(Agent.counter)

    def save(self, filename):
        torch.save(self.Q, filename)
    
    def load(self, filename):
        self.Q = torch.load(filename)