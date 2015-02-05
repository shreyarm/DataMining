import util
import classificationMethod
import math
import copy
import sys

'''The below class has been used from :
http://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python'''

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels):
        self.final_dict = {}
        self.label_prob_dict = {}
        self.label_prob_dict_TT = {}
        self.feat_val = [0,1]
        self.prob_dict = {}
        self.tt_final_dict = {}
        self.valid = {}
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 0  # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False  # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        self.features = trainingData[0].keys()  # this could be useful for your code later...

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
            self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
        else:
            # two choices, either we have smoothing or we don't
            if self.k == 0:
                self.justTrain(trainingData, trainingLabels)
            else:
                self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, [self.k])

    def justTrain(self, trainingData, trainingLabels):  # trainingData = features and trainingLabels = labels
        """
           Trains the classifier by collecting counts over the training data, and
        stores the (unsmoothed) estimates so that they can be used to classify.

        trainingData and validationData are lists of n_feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"

        label_count = util.Counter()
        c = 0
        for x in trainingLabels: # for loop
            label_count[x] += 1
            c += 1

        final_dict = {}

        for n_feature in range(0, len(self.features)):
            feature = self.features[n_feature]
            final_dict[feature] = {}

            for data_dict in range(0, len(trainingData)):
                single_data_dict = trainingData[data_dict]

                if feature in single_data_dict:
                    feature_value = trainingData[data_dict][feature]
                    label = trainingLabels[data_dict]
                    value = final_dict.get(feature)    # value1 = 0:{0:1} feature_value = 0

                    if feature_value not in value:
                        final_dict[feature][feature_value] = {}
                        final_dict[feature][feature_value][label] = 1
                    else:
                        temp_value = final_dict[feature][feature_value]
                        if label not in temp_value:
                            final_dict[feature][feature_value][label] = 1
                        else:
                            final_dict[feature][feature_value][label] += 1

        self.final_dict = final_dict

        prob_dict = final_dict
        self.prob_dict = prob_dict

        for tuple in self.prob_dict:
            for zerone in final_dict[tuple]:
                label_dict = final_dict[tuple][zerone]
                for key in label_dict:
                    num = label_dict.get(key)
                    dem = label_count.get(key)
                    result = (float)(num)/(float)(dem)
                    label_dict[key] = result

        for c_value in label_count:
            n = label_count.get(c_value)
            d = c
            r = float(n)/float(d)
            self.label_prob_dict[c_value] = r

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.
        If kgrid just contains one value, use it for smoothing but then there's no need to evaluate
        on the validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"

        highest_val = 0
        k_dict = {}

        label_c = util.Counter()
        c = 0
        for x in trainingLabels: # for loop
            label_c[x] += 1
            c += 1

        for c_value in label_c:
            n = label_c.get(c_value)
            d = c
            r = float(n)/float(d)
            self.label_prob_dict[c_value] = r

        final_dict = {}

        for k in kgrid:
        # probability of the data
            for n_feature in range(0, len(self.features)):
                feature = self.features[n_feature]
                final_dict[feature] = {}

                for data_dict in range(0, len(trainingData)):
                    single_data_dict = trainingData[data_dict]

                    if feature in single_data_dict:
                        feature_value = trainingData[data_dict][feature]
                        label = trainingLabels[data_dict]
                        value = final_dict.get(feature)    # value1 = 0:{0:1} feature_value = 0

                        if feature_value not in value:
                            final_dict[feature][feature_value] = {}
                            final_dict[feature][feature_value][label] = 1
                        else:
                            temp_value = final_dict[feature][feature_value]
                            if label not in temp_value:
                                final_dict[feature][feature_value][label] = 1
                            else:
                                final_dict[feature][feature_value][label] += 1

            self.final_dict = final_dict

            for n_feature in range(0, len(self.features)):  # all features are present
                fe = self.features[n_feature]
                for feat_va in range(0, len(self.feat_val)):
                    va = self.feat_val[feat_va]
                    if va not in self.final_dict[fe]: #value (0 or 1) not in dictionary
                        self.final_dict[fe][va] = {}
                        for l in self.legalLabels:
                            self.final_dict[fe][va][l] = k
                    else: # value 0 or 1 present in dict
                        for n_label in self.legalLabels: # checking for labels
                            if n_label not in self.final_dict[fe][va]:
                                self.final_dict[fe][va][n_label] = k
                            else:
                                self.final_dict[fe][va][n_label] = self.final_dict[fe][va][n_label] + k

            for tuple in self.final_dict:
                for tt_label in self.final_dict[tuple]:
                    label_val = self.final_dict[tuple][tt_label]
                    for key in label_val:
                        num = label_val.get(key)
                        dem = label_c.get(key)

                        f_dem = (float)(2 * k) + (float)(dem)
                        result = (float)(num)/(float)(f_dem)
                        final_dict[tuple][tt_label][key] = result

            check = []
            self.valid = []  # Log valid are stored for later data analysis (autograder).
            for datum in validationData:
                val = self.calculateLogJointProbabilities(datum)
                check.append(val.argMax())
                self.valid.append(val)

            v_ctr = 0
            v_tot = 0

            for v_label in range(0, len(validationLabels)):
                if validationLabels[v_label] == check[v_label]:
                    v_ctr += 1
                v_tot +=1
            result = 100*(float(v_ctr)/float(v_tot))
            k_dict[k] = result

        k = max(k_dict, key=k_dict.get)

        for n_feature in range(0, len(self.features)):
                feature = self.features[n_feature]
                final_dict[feature] = {}

                for data_dict in range(0, len(trainingData)):
                    single_data_dict = trainingData[data_dict]

                    if feature in single_data_dict:
                        feature_value = trainingData[data_dict][feature]
                        label = trainingLabels[data_dict]
                        value = final_dict.get(feature)    # value1 = 0:{0:1} feature_value = 0

                        if feature_value not in value:
                            final_dict[feature][feature_value] = {}
                            final_dict[feature][feature_value][label] = 1
                        else:
                            temp_value = final_dict[feature][feature_value]
                            if label not in temp_value:
                                final_dict[feature][feature_value][label] = 1
                            else:
                                final_dict[feature][feature_value][label] += 1

        self.final_dict = final_dict

        for n_feature in range(0, len(self.features)):  # all features are present
            fe = self.features[n_feature]

            for feat_va in range(0, len(self.feat_val)):
                va = self.feat_val[feat_va]
                if va not in self.final_dict[fe]: #value (0 or 1) not in dictionary
                    self.final_dict[fe][va] = {}
                    for l in self.legalLabels:
                        self.final_dict[fe][va][l] = k
                else: # value 0 or 1 present in dict
                    for n_label in self.legalLabels: # checking for labels
                        if n_label not in self.final_dict[fe][va]:
                            self.final_dict[fe][va][n_label] = k
                        else:
                            self.final_dict[fe][va][n_label] = self.final_dict[fe][va][n_label] + k

        # finding the probability for the training data
        for tuple in self.final_dict:

            for tt_label in self.final_dict[tuple]:
                label_val = self.final_dict[tuple][tt_label]

                for key in label_val:
                    num = label_val.get(key)
                    dem = label_c.get(key)
                    f_dem = (float)(2 * k) + (float)(dem)
                    result = (float)(num)/(float)(f_dem)
                    final_dict[tuple][tt_label][key] = result

        check = []
        self.valid = []  # Log valid are stored for later data analysis (autograder).
        for datum in validationData:
            val = self.calculateLogJointProbabilities(datum)
            check.append(val.argMax())
            self.valid.append(val)


        self.final_dict = final_dict

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        DO NOT modify this method.
        """
        guesses = []
        self.posteriors = []  # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
        """
        logJoint = util.Counter()
        "*** YOUR CODE HERE ***"

        for label in self.legalLabels:  # runs the number of times the features are encountered
            status = 0
            for feat in datum: #feat is the tuple
                feat_val = datum.get(feat)
                if feat in self.final_dict:
                    if feat_val in self.final_dict[feat]:
                        for valid_label in self.final_dict[feat][feat_val]:
                            if label in self.final_dict[feat][feat_val]:
                                total_label_prob = self.label_prob_dict[label] # CHECK
                                in_label_prob = self.final_dict[feat][feat_val][label] # error in this line :(
                                logJoint[label] = logJoint[label] + math.log(in_label_prob)

            logJoint[label] = logJoint[label] + math.log(total_label_prob)

        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)
        """
        featuresOdds = []
        odd_ratio_dict = {}
        dictlist = []

        "*** YOUR CODE HERE ***"
        for f in self.features:
            odd_ratio_num = self.final_dict[f][1][label1]
            odd_ratio_demo = self.final_dict[f][1][label2]
            odd_ratio = float(odd_ratio_num)/float(odd_ratio_demo)
            odd_ratio_dict[f] = odd_ratio
        for key, value in odd_ratio_dict.items():
            temp = [value, key]
            dictlist.append(temp)
        dictlist.sort(reverse=True)
        for i in range(0, 100):
            featuresOdds.append(dictlist[i][1])
        #print "FeaturesOdds list : ", featuresOdds
        return featuresOdds