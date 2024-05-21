import torch 
import torch.nn as nn
import torch.nn.functional as F

from Environment.State import State
from Environment.Actions.Action import Action

# Needs to implement DQN properly with target and policy net. 
class Agent: 
    # Output needs to be of size 3 for action: (id, location, type)
    NETWORK = [4, 50, 50, 3] 

    def __init__(self):
        self.Q = DQN(Agent.NETWORK)

    def pickAction(self, state: State):
        print("Agent.pickAction NOT IMPLEMENTED YET")
        return Action((1, 1, 1))

class DQN(nn.Module):
    def __init__(self, layer_sizes:list[int]):
        super(DQN, self).__init__()
        self.layers = nn.ModuleList([nn.Linear(layer_sizes[i], layer_sizes[i+1]) for i in range(len(layer_sizes)-1)])
    
    def forward (self, x:torch.Tensor)->torch.Tensor:
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        x = self.layers[-1](x)
        return x
