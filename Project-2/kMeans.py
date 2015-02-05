__author__ = 'cindi'

import sys
import random
from sklearn import preprocessing
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np
from copy import deepcopy


def calc_dist(X1, X2):
    """
    Calculate the Euclidean distance between the two given vectors
    :param X1: d-dimensional vector
    :param X2: d-dimensional vector
    :return: Euclidean distance between X1 and X2
    """
    # ## TODO: Your code here (Q1)
    sumSq = 0.0
    dim = len(X1)

    #add up the squared differences
    for i in range(dim):
        sumSq += (X1[i]-X2[i])**2
        #take the square root of the result

    euclidean_distance = sumSq**0.5
    return euclidean_distance


def centroid(C):
    """
    Compute the centroid of the given list of vectors
    :param C: List of d-dimensional vectors
    :return: mean(C)
    """
    # ## TODO: Your code here (Q2)
    dict = {}
    mean_dict = {}
    mean_list =[]
    dim = len(C[0])

    for d in range(0,dim):
        dict[d] = []
        #mean_dict[d] = []

    for i in range(0,len(C)):
        for d in range(0,dim):
            #print C[i][d]
            dict[d].append(C[i][d])

    for d1 in range(0,len(dict)):
        mean_dict[d1] = np.mean(dict[d1])
        mean_list.append(mean_dict[d1])

    return mean_list

class kMeans():
    """
    This defines the kMeans clustering algorithm.
    """

    def __init__(self, k, max_iter=300):
        """

        :param k: the number of clusters
        :param max_iter: the maximum number of iterative updates to make to the cluster assignments;
          You can also stop before max_iter if you are satisfied with your clustering
        :return:
        """
        self.k = k
        self.iterations = max_iter

        #feel free to change the below assignment, but not the variable name,
        # this is where you should store your clusters
        self.clusters = None
        # this is where you should store your scaling object (see project description)
        self.scaler = None
        #you may add other class variables here
        self.centroid_dictionary ={}
        self.final_dict = {}

    def normalize(self, data):
        """
        Initializes self.scaler and returns a normalized version of the data
        :param data:
        :return:
        """
        # ## TODO: Your code here (Q3)
        self.scaler = 0
        s = preprocessing.MinMaxScaler()
        #self.scaler = deepcopy(s)
        final_data = s.fit_transform(data)
        self.scaler = s.fit(data)

        return final_data

    def fit(self, data):
        """
        Find self.k clusters
        :param data: Unlabeled training data (list of x1...xd vectors)
        :return: None is fine, but feel free to return something meaningful to calling program
        """
        # ## TODO: Your code here (Q4)
        #print("data",data)

        k = self.k
        norm_data = self.normalize(data)
        max_index = int(k)
        min_index = 0
        clustering_limit = int(self.iterations)
        clustered_dict = {}

        for j in range(max_index):
            clustered_dict[j] = []

        '''
        Created the initial clusters randomly
        '''
        for d in range(len(norm_data)):  #data is the training data 150
            random_index = random.randrange(min_index, max_index)
            data_np_array = np.array(norm_data[d])
            clustered_dict[random_index].append(data_np_array)

        for i in range(0,max_index):
            if len(clustered_dict[i]) == 0:
               clustered_dict[0] = norm_data[0]

        '''
        Finding the centroid of each list in the dictionary
        '''
        centroid_dict = {}

        for r in range(0,max_index):
            centroid_dict[r] = []
            c = centroid(clustered_dict[r])
            centroid_dict[r] = c

        w_eval = 0
        sum = 0
        '''
        recursively finding and re-assigning the new clusters
        '''
        #print "Below are the progress of the clusters, till it either reaches the maximum cluster iteration limit ", clustering_limit, "or there is not further change in the cluster centroids."
        #print("------------------------")
        for i in range(0, clustering_limit):  # runs iteration time, default is 300
            for j in range(max_index):  # initializing the dictionary to store the new values on the cluster
                clustered_dict[j] = []
            for points in range(0, len(norm_data)):  # 150
                dist_list = []
                for cen in range(len(centroid_dict)):  # cen the cluster number = 3 = no of cluster times
                    e_u = calc_dist(norm_data[points], centroid_dict[cen])
                    dist_list.append(e_u)
                min_val = min(dist_list)
                index_of_min_dist = dist_list.index(min_val)
                clustered_dict[index_of_min_dist].append(np.array(norm_data[points]))

            # calculating the new centroid
            centroid_temp = deepcopy(centroid_dict)
            #ceto = 0.0
            for r in range(0,max_index):
                try:
                    ceto = centroid(clustered_dict[r])
                    centroid_dict[r] = ceto
                except IndexError:
                    continue


            #print "Cluster for iteration ", i
            #for po in range(len(clustered_dict)):
                # print clustered_dict[po]
                #print "Cluster[",po,"]: ", len(clustered_dict[po])
            #print("------------------------")

            if centroid_dict == centroid_temp:
                #print "Centroids is same as the previous one, hence breaking out of loop at: ", i
                break
        #print "This result is for total number of cluster: ", max_index
        #print "Total number of training data set used: ", len(norm_data)
        self.centroid_dictionary = centroid_dict

    def predict(self, data):
        """ Assumes that fit has already been called to create your clusters
        :param data: New data points
        :return: A list containing the index in range(k) to which each X in data should be assigned
        """
        # ## TODO: Your code here (Q5)
        centroid_dict = self.centroid_dictionary

        # don't forget to apply self.scaler!

        norm_data = self.scaler.transform(data)

        predict_dict = []

        for points in range(0, len(norm_data)):  # 150
            dist_list = []
            for cen in range(len(centroid_dict)):  # cen the cluster number = 3 = no of cluster times
                e_u = calc_dist(norm_data[points], centroid_dict[cen])
                dist_list.append(e_u)
                min_val = min(dist_list)
                index_of_min_dist = dist_list.index(min_val)
                #print index_of_min_dist
            predict_dict.append(index_of_min_dist)

        #print "Predict Dict: ",  predict_dict
        #scaler = self.scaler
        return predict_dict

## DO NOT change this method
def eval_clustering(labels_true, labels_guess):
    """
    Given the ground truth and our guessed clustering assignment, use the Adjusted Rand index to measure
    assignment similarity
    :return: Rand Index
    """
    return metrics.adjusted_rand_score(labels_true, labels_guess)


def compare_sklearn(x_train, x_test, y_train, y_test, k):
    """
    Apply the KMeans algorithm of sklearn to the input data set, and return its "accuracy"
    of assigning labels to clusters. Use k as the number of clusters learned by sklearn's KMeans
    :param x_train:
    :param x_test:
    :param y_train:
    :param y_test:
    :return: Accuracy of the clustering assignments, using the training set accuracy if test set is empty
    """
    # ## TODO: Your code here (Q6)
    #print "y_test", y_test
    # this code will call eval_clustering; see main for how to use

    s = preprocessing.MinMaxScaler()
    s = s.fit(x_train)
    norm_x_train = s.transform(x_train)

    clu = KMeans(n_clusters = k)
    clu = clu.fit(norm_x_train)

    if len(x_test) == 0:
        clu = clu.predict(norm_x_train)
        return eval_clustering(clu, y_train)
    else:
        norm_x_test = s.transform(x_test)
        clu = clu.predict(norm_x_test)
        return eval_clustering(clu, y_test)