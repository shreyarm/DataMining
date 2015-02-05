import sys
import copy

d= {'a':2,'b':5,'c':3}
print max(d, key=d.get)

sys.exit(0)
#'b'
list = [[5, (7,3)], [6,(20,25)], [4, (9,6)]]

list2 = copy.deepcopy(list)

list[0] = [10, (10,3)]

print list
print list2





























'''for i in range(0, 99):
    print i
sys.exit(0)

features = [(2,5),(7,3),(27,8),(20,25)] #self.feature

trainingData = [{(7,3):1 , (16,14):1, (27,8):0, (2,5):0},
                {(20,25):1, (7,3):0, (2,5):0, (27,8):1},
                {(1,0):0, (2,5):0, (7,3):0, (20,25):1},
                {(2,5):1, (7,3):0, (27,8):0, (20,25):0},
                {(7,3):1 , (16,14):1, (27,8):0, (2,5):0},
                {(20,25):1, (7,3):0,(2,5):0, (27,8):1},
                {(1,0):0, (2,5):0, (7,3):0, (20,25):1},
                {(2,5):1, (7,3):0, (27,8):0, (20,25):0}]

legalLabels = [0,1,2,3]
trainingLabels = [0,3,2,1,3,2,1,0,1]
legal_feat_val = [0,1]
k =2

tt_final_dict = {}

for n_feature in range(0, len(features)):
    feature = features[n_feature]
    tt_final_dict[feature] = {}

    for data_dict in range(0, len(trainingData)):
        single_data_dict = trainingData[data_dict]

        if feature in single_data_dict:
            feature_value = trainingData[data_dict][feature]
            label = trainingLabels[data_dict]
            value = tt_final_dict.get(feature)    # value1 = 0:{0:1} feature_value = 0

            if feature_value not in value:
                tt_final_dict[feature][feature_value] = {}
                tt_final_dict[feature][feature_value][label] = 1
            else:
                temp_value = tt_final_dict[feature][feature_value]
                if label not in temp_value:
                    tt_final_dict[feature][feature_value][label] = 1
                else:
                    tt_final_dict[feature][feature_value][label] += 1

for n_feature in range(0, len(features)):  # all features are present
    fe = features[n_feature]
    #print fe
    for feat_val in range(0, len(legal_feat_val)):
        va = legal_feat_val[feat_val]
        #print va
        #print tt_final_dict[feature]
        if va not in tt_final_dict[fe]:
            tt_final_dict[fe][va] = {}
            for l in legalLabels:
                tt_final_dict[fe][va][l] = k
        else:
            for n_label in legalLabels:
                if n_label not in tt_final_dict[fe][va]:
                    tt_final_dict[fe][va][n_label] = k
                else:
                    tt_final_dict[fe][va][n_label] = tt_final_dict[fe][va][n_label] + k

print tt_final_dict'''