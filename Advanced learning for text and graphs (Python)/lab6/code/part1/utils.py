"""
Deep Learning on Graphs - ALTEGRAD - Jan 2021
"""

import scipy.sparse as sp
import numpy as np
import torch
import torch.nn as nn

def normalize_adjacency(A):
    ############## Task 1
    I = sp.identity(len(A.toarray())) 
    A_hat = A + I
    D = np.diag(1/(np.sum(A_hat.toarray(),axis = 1)))
    A_normalized = sp.csr_matrix(D@A_hat)
    ##################
    # your code here #
    ##################
    return A_normalized


def sparse_to_torch_sparse(M):
    """Converts a sparse SciPy matrix to a sparse PyTorch tensor"""
    M = M.tocoo().astype(np.float32)
    indices = torch.from_numpy(np.vstack((M.row, M.col)).astype(np.int64))
    values = torch.from_numpy(M.data)
    shape = torch.Size(M.shape)
    return torch.sparse.FloatTensor(indices, values, shape)


def loss_function(z, adj, device):
    mse_loss = nn.MSELoss()

    ############## Task 3
    indices = adj._indices()
    y_pred = []
    y = []
    y_pred.append(torch.sum(torch.mul(z[indices[0,:],:], z[indices[1,:],:]), dim=1))
    y.append(torch.ones(indices.size(1)).to(device))
    random_indices = torch.randint(z.size(0), indices.size())
    y_pred.append(torch.sum(torch.mul(z[random_indices[0,:],:], z[random_indices[1,:],:]), dim=1))
    y.append(torch.zeros(random_indices.size(1)).to(device))
    y_pred = torch.cat(y_pred, dim=0)
    y = torch.cat(y, dim=0)
    ##################
    # your code here #
    ##################
    
    loss = mse_loss(y_pred, y)
    return loss