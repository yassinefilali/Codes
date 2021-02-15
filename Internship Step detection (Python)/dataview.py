import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df=pd.read_csv(r"C:\Users\Yassine\Desktop\GaitData\1-1.csv")
x=df.describe()
fig,ax=plt.subplots(4,2)
fig.suptitle('Signals for 1-1')
names=df.columns
for i in range(4):
    for j in range(2):
        data=df.iloc[:,i+j]
        ax[i,j].plot(data)
        ax[i,j].set_title(names[i+j])


