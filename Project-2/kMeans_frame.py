__author__ = 'cindi'

import sys
from sklearn import datasets
from sklearn.cross_validation import train_test_split
import kMeans


def default(str):
    return str + ' [Default: %default]'


def readCommand(argv):
    "Processes the command used to run from the command line."
    from optparse import OptionParser

    parser = OptionParser(USAGE_STRING)

    parser.add_option('-d', '--data', help=default('Dataset to use'), choices=['digits', 'iris'], default='iris')
    parser.add_option('-t', '--training', help=default('The size of the training set'), default=150, type="int")
    parser.add_option('-k', '--num_clusters', help=default("Number of clusters"), default=3, type="int")
    parser.add_option('-s', '--sk_compare', help=default("Compare to sklearn"), action="store_true", default=False)
    #feel free to add an option to change the max_iter parameter

    options, args = parser.parse_args(argv)

    if options.data != 'iris' and options.data != 'digits':
        print "Unknown dataset", options.data
        print USAGE_STRING
        sys.exit(2)

    if options.training < 0:
        print "Training set size should be zero or a positive integer (you provided: %d)" % options.training
        print USAGE_STRING
        sys.exit(2)

    if options.num_clusters <= 0:
        print "Please provide a positive number for number of clusters (you provided: %f)" % options.smoothing
        print USAGE_STRING
        sys.exit(2)

    return options

USAGE_STRING = """
  USAGE:      python kMeans.py <options>
  EXAMPLES:   (1) python kMeans.py
                  - trains the kMeans algorithm on the sklearn iris dataset with k=3
                  using the iris training examples and print the cluster membership on the same data

              (2) python kMeans.py  -d digits -t 1250 -k 10
                  - would run kMeans on a randomly chosen set of 1250 training examples of digits, with k=10, and
                  print the cluster membership on the held out (test/unseen) examples from digits
                 """


def runClustering(options):
    if options.data == 'iris':
        data_dict = datasets.load_iris()
    else:
        data_dict = datasets.load_digits()

    rawTrain = data_dict.data
    if options.training > len(rawTrain):
        print "Training set size you provided is more than the number of examples available " \
              "(you provided: %d, num exs: %d" % (options.training, len(rawTrain))
        sys.exit(2)

    if options.training == len(rawTrain):
        x_train = rawTrain
        x_test = rawTrain
        y_train = data_dict.target
        y_test = data_dict.target
    else:
        x_train, x_test, y_train, y_test = train_test_split(rawTrain, data_dict.target, train_size=options.training)

    clf = kMeans.kMeans(k=options.num_clusters)
    print "Training..."
    clf.fit(x_train)

    print "Testing..."
    if len(x_test) > 0:
        guess_clusters = clf.predict(x_test)
        truth = y_test
    else:
        guess_clusters = clf.predict(x_train)
        truth = y_train

    correct = kMeans.eval_clustering(truth, guess_clusters)
    print "Score for your partitioning with %d training examples and %d test examples: %.3f " \
          % (len(x_train), len(x_test), correct)

    if options.sk_compare:
        sk_correct = kMeans.compare_sklearn(x_train, x_test, y_train, y_test, options.num_clusters)
        print "Score for sklearn's partitioning with %d training examples and %d test examples: %.3f " \
              % (len(x_train), len(x_test), sk_correct)
        if sk_correct > correct:
            print "You lose!"
        else:
            print "You win!"

if __name__ == '__main__':
    # Read input
    options = readCommand(sys.argv[1:])
    # Run clustering
    runClustering(options)