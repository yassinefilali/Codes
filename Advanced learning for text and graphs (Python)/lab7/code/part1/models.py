"""
Learning on Sets - ALTEGRAD - Jan 2021
"""

import torch
import torch.nn as nn

class DeepSets(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim):
        super(DeepSets, self).__init__()
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.tanh = nn.Tanh()

    def forward(self, x):
        
        ############## Task 3
        x=self.embedding(x)
        x=self.fc1(x)
        x=self.tanh(x)
        x=torch.sum(x,1)
        x=self.fc2(x)
        ##################
        # your code here #
        ##################
        
        return x.squeeze()


class LSTM(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim):
        super(LSTM, self).__init__()

        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        
        ############## Task 4
        x=self.embedding(x)
        x=self.lstm(x)
        x=self.fc(x[1][-1])
        ##################
        # your code here #
        ##################
        
        return x.squeeze()