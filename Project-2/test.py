import numpy as np
import matplotlib.pyplot as plt
import random
N=50
X=[np.random.uniform(0,1,N*2)]
X=np.reshape(X,(50,2))
X[0:25,1]=X[0:25,1]+3
X[0:25,1]
plt.plot(X[:,0],X[:,1])
plt.plot(X[:,1],X[:,0])
plt.show()