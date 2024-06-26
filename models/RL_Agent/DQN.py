import os
import time

import torch
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
import copy,datetime
from models.RL_Agent.Neural_Networks import DQN_neural_network
from pathlib import Path

from collections import deque
import numpy as np
import random
import pickle
# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
class DQN:
    def __init__(self,state_size,action_size,model_dir,name,learning=True) -> None:
        self.learning = learning
        self.BATCH_SIZE = 256
        self.GAMMA = 1
        self.MEM_CAPACITY = 5000
        self.min_experiance = 20
        self.learn_every = 1  # no. of experiences between updates to Q_online
        self.sync_every = 100  # no. of experiences between Q_target & Q_online sync
        self.save_every = 100
        self.learning_rate = 0.00005
        self.name = name
        save_file_model = os.path.join(model_dir, "Q_value.model")
        save_file_mem = os.path.join(model_dir, "Q_value.mem")
        try: 
            self.Q_value = DQN_neural_network.load_model(save_file_model)
            if self.Q_value is None:
               self.Q_value = DQN_neural_network(state_size,action_size)
            print(f"Model loaded from {save_file_model}")
        except:
            print('No saved model found, starting from scratch...')
            self.Q_value = DQN_neural_network(state_size,action_size)
        self.memory = DQN.load_mem(model_dir)
        if self.memory is None:
            self.memory = deque(maxlen=self.MEM_CAPACITY)

        try: 
            os.mkdir(model_dir)
        except FileExistsError:
            pass 
        # if not os.path.exists(save_file_model):
        #     os.makedirs(save_file_model.split('Q_value.model')[0])

        self.optimizer = torch.optim.Adam(self.Q_value.parameters(), lr=self.learning_rate)
        self.loss_fn = torch.nn.SmoothL1Loss()
        self.save_dir_model = save_file_model
        self.save_dir_mem = save_file_mem
        pass

    def save(self):
        print('saving...')

        save_path = (
            self.save_dir_model
        )
        torch.save(
            self.Q_value,
            save_path
        )

    def save_mem(self):
        with open(self.save_dir_mem,"wb") as f:
            pickle.dump(self.memory,f)

    
    def load_mem(path):
        try:
            path = os.path.join(path,"Q_value.mem")
            with open(path,"rb") as f:
                data = pickle.load(f)

                return data
        except:
            return None


    def tune_network(self,curr_step):
        if curr_step % self.sync_every == 0:
  
  
            self.sync_Q_target()
        if curr_step % self.save_every == 0 and self.learning:
            self.save()
            self.save_mem()

        if curr_step < self.min_experiance:
            return None

        # Sample from memory
        state, next_state, reward,size = self.recall()
        if state is None:
            return None
        # Get TD Estimate   
        td_est = self.td_estimate(state,size)
        

        # Get TD Target
        reward = reward.squeeze()
        td_tgt = self.td_target(next_state, reward,size)


        
        # Backpropagate loss through Q_online
        loss = self.update_Q_online(td_est.squeeze(), td_tgt.squeeze())

        return loss

    def get_Q_value(self,state):
        state = state.clone().detach()
        state = state.unsqueeze(0)


        current_Q = self.Q_value(state, model="online")
        return current_Q.detach().numpy()

    def td_estimate(self, state,size):
        current_Q = self.Q_value(state, model="online")[
            np.arange(0, size)
        ]  # Q_online(s,a)

        return torch.max(current_Q,1)[0].unsqueeze(1)

    @torch.no_grad()
    def td_target(self, next_Q, reward,size):
        return (reward +self.GAMMA * next_Q).float()

    def update_Q_online(self, td_estimate, td_target):

        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward(retain_graph=True)
        self.optimizer.step()
        return loss.item()

    def sync_Q_target(self):
        self.Q_value.target.load_state_dict(self.Q_value.online.state_dict())


    def cache(self, state, next_state, reward):
        """
        Store the experience to self.memory (replay buffer)

        Inputs:
        state (LazyFrame),
        next_state (LazyFrame),
        action (int),
        reward (float),
        done(bool))
        """
        reward = torch.tensor([reward])

        self.memory.append((state, next_state, reward))

    def recall(self):
        """
        Retrieve a batch of experiences from memory
        """
        size = min(self.BATCH_SIZE,len(self.memory))
        if size < 1:
            return None,None,None,None
        batch = random.sample(self.memory, size)
        state, next_state, reward = map(torch.stack, zip(*batch))
        return state, next_state, reward,size