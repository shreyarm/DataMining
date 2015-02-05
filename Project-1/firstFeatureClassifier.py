from scipy.fftpack.basic import _datacopied
import util
import classificationMethod


class firstFeatureClassifier(classificationMethod.ClassificationMethod):
    """
    This defines the classifier that always predicts on the basis of
      the first feature only.  In particular, we maintain two
      predictors: one for when the first feature is 0, one for when the
      first feature is 1.
    """

    def __init__(self, legalLabels):
        # if we haven't been trained, always return 1
        self.classForZero = 1
        self.classForOne = 1
        self.type = "firstFeatureClf"

    def train(self, data, labels, validationData, validationLabels):
        """
        Just figure out what the most frequent class is for each value of X[:,0]
        and store it.
        Ignores validationData & validationLabels
        """
        # ## TODO: Your code here
        count0 = util.Counter()
        count1 = util.Counter()

        ctr1 = 0
        ctr0 = 0

        for d in data:
            # for d1 in d:
            if d[(0, 0)] == 1:
                #print d1.get("(0,0)")
                count1[labels[ctr1]] += 1
                ctr1 += 1
                print "count 1:", count1
            elif d[(0, 0)] == 0:
                count0[labels[ctr0]] += 1
                ctr0 += 1
                print "count 0: ", count0
        self.classForOne = count1.argMax()
        self.classForZero = count0.argMax()
        # print "Count of the d is: ",

    def classify(self, testData):
        """
        Check the first feature and make a classification decision based on it

        """
        # ## TODO: Your code here
        f_list = []
        for i in testData:
            #for j in i:
            if i[(0, 0)] == 0:
                f_list.append(self.classForZero)
            elif i[(0, 0)] == 1:
                f_list.append(self.classForOne)
        return f_list