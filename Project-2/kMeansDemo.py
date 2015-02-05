__author__ = 'cindi'
#http://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
# andhttp://blog.mpacula.com/2011/04/27/k-means-clustering-example-python/

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
import pylab

#two ways of initializing our data
def init_board(N):
    X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(N)])
    return X


def init_board_gauss(N, k):
    n = float(N)/k
    X = []
    for i in range(k):
        c = (random.uniform(-1, 1), random.uniform(-1, 1))
        s = random.uniform(0.05,0.5)
        x = []
        while len(x) < n:
            a, b = np.array([np.random.normal(c[0], s), np.random.normal(c[1], s)])
            # Continue drawing points from the distribution in the range [-1,1]
            if abs(a) < 1 and abs(b) < 1:
                x.append([a,b])
        X.extend(x)
    X = np.array(X)[:N]
    return X

#use standard init
kmeans = KMeans()

#create data
num_pts = 200
data_clusts = 3

train = init_board(num_pts)
kmeans.fit(train)

#how good is our "score"?
print metrics.silhouette_score(train, kmeans.labels_)

#now do "prettier" data
train_nice = init_board_gauss(num_pts, data_clusts)
kmeans.fit(train_nice)

#how good is our "score"?
print metrics.silhouette_score(train_nice, kmeans.labels_)

#try with a "better" k
kmeans_3 = KMeans(n_clusters=data_clusts)
kmeans_3.fit(train_nice)
print metrics.silhouette_score(train_nice, kmeans_3.labels_)

#plot data
clust_memb = kmeans_3.labels_
colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in clust_memb])

pylab.scatter(train_nice[:,0], train_nice[:,1], c=colors)
centers = kmeans_3.cluster_centers_
pylab.scatter(centers[:,0],centers[:,1], marker='o', s=500,linewidths=2, c='none')
pylab.scatter(centers[:,0],centers[:,1], marker='x', s=500,linewidths=2)