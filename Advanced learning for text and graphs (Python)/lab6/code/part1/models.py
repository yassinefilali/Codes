"""
Deep Learning on Graphs - ALTEGRAD - Jan 2021
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class GAE(nn.Module):
    """GAE model"""
    def __init__(self, n_feat, n_hidden_1, n_hidden_2, dropout):
        super(GAE, self).__init__()

        self.fc1 = nn.Linear(n_feat, n_hidden_1)
        self.fc2 = nn.Linear(n_hidden_1, n_hidden_2)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()

    def forward(self, x_in, adj):
        ############## Task 2
        x = torch.mm(adj, x_in)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = torch.mm(adj, x)
        x = self.fc2(x)
        x = self.relu(x)
        ##################
        # your code here #
        ##################

        return x