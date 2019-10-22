import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np;

data = np.load("compress.npy");

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(data[:,0], data[:,1], data[:,2]);
ax.scatter( 0.09507311,0.45015806,0.99999809,c='b');
plt.show();
