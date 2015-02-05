import util
import classificationMethod
import collections


class zeroR(classificationMethod.ClassificationMethod):
    """
    zeroR is a very simple classifier: for
    every test instance presented to it, the classifier returns
    the label that was seen most often in the training data.
    """

    def __init__(self, legalLabels):
        # if we haven't been trained, assume most frequent class is 1
        self.guess = 1
        self.type = "mostfrequent"

    def train(self, data, labels, validationData, validationLabels): # data x training, y_training
        """
        Find the most common label in the training data.
        Ignores validationData & validationLabels
        """
        # ## TODO: Your code here
        count = util.Counter()

        print 'Labels of the data is:', labels #printing all the labels from which the frequency has to be found

        for x in labels: # for loop
            count[x] += 1

        print count
        val = count.argMax()
        self.guess = val
        print val

    def classify(self, testData): #x test
        """
        Classify all test data as the most common label.
        """
        # ## TODO: Your code here
        #testData.key()

        a = []  # a is a blank list
        for i in range(len(testData)):
            a.append(self.guess)
        #print a
        return a

