"""
Learning on Sets - ALTEGRAD - Jan 2021
"""

import numpy as np


def create_train_dataset():
    n_train = 100000
    max_train_card = 10

    ############## Task 1
    X_train = []
    y_train = []
    for i in range(n_train):
        size = np.random.randint(1,max_train_card+1)
        sample = np.random.randint(1,max_train_card+1,size).tolist()
        if size<max_train_card:
            sample = np.concatenate(( [0]*(max_train_card-size) ,sample))
        
        X_train.append(np.array(sample))
        y_train.append(np.sum(sample))
    return X_train, y_train



def create_test_dataset():
 	
    ############## Task 2
    max_test_card = 10
    
    X_test = []
    y_test = []
    for size in range(5,105,5):
        s = []
        t = []
        for i in range(10000):
            sample = np.random.randint(1,max_test_card+1,size).tolist()
            s.append(np.array(sample))
            t.append(np.sum(sample))
            
            
        X_test.append(np.array(s))
        y_test.append(t)
  
    return X_test, y_test



