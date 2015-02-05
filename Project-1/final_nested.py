__author__ = 'shreyarajani'
import util

if __name__ == '__main__':

    features = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]  # 9 features

    trainingData = [{(0, 0): 1, (0, 1): 1, (1, 2): 0, (2, 0): 0},
                    {(0, 0): 0, (0, 1): 1, (1, 2): 1, (1, 0): 0},
                    {(1, 0): 1, (1, 1): 0, (1, 2): 0, (2, 0): 1},
                    {(0, 1): 1, (2, 1): 1, (1, 2): 1, (1, 1): 0},
                    {(0, 2): 0, (0, 1): 1, (1, 2): 0, (2, 0): 0},
                    {(1, 2): 1, (1, 1): 0, (2, 1): 1, (1, 0): 1}]
    trainingLabels = [0, 1, 2, 3, 4, 5]

    dict = {}
    ctr = 0

    for n_features in features:  # individual (0,0, (0,1)

        dict[n_features] = {}  # eg: (2,5), (3,4)

        #print n_features

        for data in trainingData:  # data is the individual dictionary in training data
            if n_features in data:  # checking if that feature is in the training data or not
                #trainingData[ctr][data_index]

                #We have to check if the labels is present or not
                if n_features in dict == {}:
                    present_feature = dict[n_features]
                    if present_feature in dict[n_features]:
                        print "Hello"


                #for labels in trainingLabels:
                    #dict[n_features][dict.get(n_features)][labels] = {}
            #else:
                #dict[n_features][data.get(n_features)] = {}



    #print dict
                #ctr =+ 1