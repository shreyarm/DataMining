__author__ = 'shreyarajani'

import numpy as np
from sklearn import datasets
from sklearn.cross_validation import KFold
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import random
import zeroR

if __name__ == '__main__':
    iris = datasets.load_iris()
    iris = load_iris()

    x_y = zip(iris.data, iris.target) #makes a list of tuples of X, Y values (this is L)

    random.shuffle(x_y) # shuffles your L
    #Now get the first elements and second elements back into X, Y for
    # selecting the examples to train & test on
    X = []
    Y = []
    ze = []
    dt =[]
    clf = DecisionTreeClassifier()
    z = zeroR.zeroR(1)

    for i in x_y:
        X.append(i[0])
        Y.append(i[1])

    X = np.array(X)
    Y = np.array(Y)

    kf = KFold(150, n_folds=10)

    for train, test in kf:
        x_training_data = X[train]
        #print "x-train", x_training_data
        #raw_input()
        y_training_data = Y[train]
        x_test_data = X[test]
        y_test_data = Y[test]

        z.train(x_training_data, y_training_data, [], [])
        guesses = z.classify(x_test_data)

        clf.fit(x_training_data, y_training_data)
        d_guesses = clf.predict(x_test_data)

        correct1 = [guesses[i] == y_test_data[i] for i in range(len(x_test_data))].count(True)
        #print str(correct1), ("correct out of " + str(len(y_test_data)) + " (%.1f%%).") % (100.0 * correct1 / len(y_test_data))
        z_p = (100.0 * correct1 / len(y_test_data))
        ze.append(z_p)

        correct2 = [d_guesses[i] == y_test_data[i] for i in range(len(y_test_data))].count(True)
        #print str(correct2), ("correct out of " + str(len(y_test_data)) + " (%.1f%%).") % (100.0 * correct2 / len(y_test_data))
        d_p = (100.0 * correct2 / len(y_test_data))
        dt.append(d_p)

    z_mean = np.mean(ze)
    print "Accuracy of zeroR: ",ze
    print "Mean accuracy of zeroR: ", z_mean,"%"

    d_mean = np.mean(dt)
    print "Accuracy of DecisionTreeClassifier: ",dt
    print "Mean of accuracy DecisionTreeClassifier: ", d_mean,"%"