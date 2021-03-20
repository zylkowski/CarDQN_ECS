import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque
import ecs


class Net(nn.Module):
    def __init__(self, input_dim, action_size, load_path=None):
        super(Net, self).__init__()
        self.input_dim = input_dim
        self.action_size = action_size

        self.fc1 = nn.Linear(input_dim, 7)
        self.fc2 = nn.Linear(7, 7)
        self.fc3 = nn.Linear(7, 6)
        self.fc4 = nn.Linear(6, action_size)

        if load_path is not None:
            self.load(self.load_path)

    def forward(self, state):
        state = state.to(torch.device("cpu"))
        state = F.relu(self.fc1(state))
        state = F.relu(self.fc2(state))
        state = F.relu(self.fc3(state))
        actions = self.fc4(state)
        return actions

    def load(self, file_path):
        self.load_state_dict(torch.load(file_path))

class DQNAgentData(ecs.Component):
    def __init__(self):
        self.state = None
        self.action = None
        self.reward = None
        self.next_state = None
        self.done = False

        self.passed_checkpoints = {}
        self.last_checkpoint_time = 0

        self.starting_position = None
        self.starting_rotation = None
        self.lifetime = 0


    def get_data_to_remember(self):
        return self.state, self.action, self.reward, self.next_state, self.done

class DQNAgent(ecs.Component):
    def __init__(self, learning_rate, input_dim, action_size, load_path=None):

        self.state_size = input_dim
        self.action_size = action_size

        self.memory = deque(maxlen=8000)

        self.GAMMA = 0.7
        self.EPSILON = 1
        self.EPSILON_DECAY = 0.998
        self.EPSILON_MIN = 0.02

        self.learning_rate = learning_rate

        self.device = torch.device('cpu')
        self.model = Net(input_dim, action_size, load_path)
        self.model = self.model.to(self.device)


        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criteria = nn.MSELoss()

    def remember(self, to_remember):
        self.memory.append(to_remember)

    def act(self, state):
        if np.random.rand() <= self.EPSILON:
            return random.randrange(self.action_size)
        with torch.no_grad():
            act_values = self.model.forward(state)
        return torch.argmax(act_values).item()

    def replay(self, batch_size):
        if batch_size <= len(self.memory):
            minibatch = random.sample(self.memory, batch_size)

            for state, action, reward, next_state, done in minibatch:

                self.optimizer.zero_grad()
                target = reward
                if not done:
                    target = (reward + self.GAMMA * torch.max(self.model.forward(next_state)).item())
                target_f = self.model.forward(state)
                print(f"target_f = {target_f}")
                target_f[0][action] = target

                loss = self.criteria(target_f, self.model.forward(state))

                loss.backward()
                self.optimizer.step()

            if self.EPSILON > self.EPSILON_MIN:
                self.EPSILON *= self.EPSILON_DECAY
            print(self.EPSILON)