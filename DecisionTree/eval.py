import argparse
from sklearn.externals import joblib
import mlUtil
import decisionTree
import random

def k_fold_eval(traind, k):
    '''See the Word doc for specifications
    '''
    test_size = int(len(traind["data"][:1000])/k)
    result_dict = {}
    #testset's precisions,recalls,accuracy
    v_precisions = []
    v_recalls = []
    v_accuracys = []
    #trainset's precisions,recalls,accuracy
    t_precisions = []
    t_recalls = []
    t_accuracys = []
    # get random id numbers in range(0,k) for a number of k
    id_ls = random.sample(xrange(0,k),k)
    for i in id_ls:
        #each time, select the i_th part of data as testset which depends on the id from random_id list
        test_set = traind["data"][:1000][i*test_size:(i+1)*test_size]
        #copy all samples/labels from data and data's labels
        train_set = traind["data"][:1000][:]
        train_labels = traind["target"][:1000][:]
        #Then delete the samples and labels which testset contains...Now,the remaining sets are the trainset
        del(train_labels[i*test_size:(i+1)*test_size])
        del(train_set[i*test_size:(i+1)*test_size])
        #fit the trainset and predict the testset
        clf = decisionTree.DecisionTree(attrib_d = data['feature_dict'], attribs = data['feature_names'],default_v="default")
        clf.fit(train_set,train_labels)
        decisionTree.printTree(clf.clf)
        train_tars = clf.predict(train_set)
        test_tars = clf.predict(test_set)
        #actual targets for testing set
        test_act = traind["target"][:1000][i*test_size:(i+1)*test_size]
        #Assume that the most common value is the positive one
        positive = decisionTree.zeroR(traind['target'][:1000])
        #init TP,TN,FP,FN
        TP = 0.0
        TN = 0.0
        FP = 0.0
        FN = 0.0
        # calculate tests' performance
        for i in range(len(test_tars)):
            if test_tars[i] == test_act[i]:
                if test_tars[i] == positive:
                    TP = TP + 1
                else:
                    TN = TN + 1
            # else, we get a false value
            else:
                if test_tars[i] == positive:
                    FP = FP + 1
                else:
                    FN = FN + 1

        if(TP+FP)==0.0:
            v_precisions.append(0.0)
        else:
            v_precisions.append(float(TP/(TP + FP)))
        if(TP+FN)==0.0:
            v_recalls.append(0.0)
        else:
            v_recalls.append((TP/(TP + FN)))
        v_accuracys.append(float((TP+TN)/len(test_act)))

        #set TP,TN,FP,FN to 0 in order calculate trainset's performance
        TP = 0.0
        TN = 0.0
        FP = 0.0
        FN = 0.0
        # For trainset...(the same as testset)
        for i in range(len(train_tars)):
            if train_tars[i] == train_labels[i]:
                if train_tars[i] == positive:
                    TP = TP + 1
                else:
                    TN = TN + 1
            # else, we get a false value
            else:
                if train_tars[i] == positive:
                    FN = FN + 1
                else:
                    FP = FP + 1
        if(TP+FP)==0.0:
            t_precisions.append(0.0)
        else:
            t_precisions.append((TP/(TP + FP)))
        if(TP+FN)==0.0:
            t_recalls.append(0.0)
        else:
            t_recalls.append((TP/(TP + FN)))
        t_accuracys.append(((TP+TN)/len(train_labels)))

    #calculate the average for each value
    v_precision = sum(v_precisions)/k
    v_recall = sum(v_recalls)/k
    v_accuracy = sum(v_accuracys)/k

    result_dict["test_precision"] = v_precision
    result_dict["test_recall"] = v_recall
    result_dict["test_accuracy"] = v_accuracy

    t_precision = sum(t_precisions)/k
    t_recall = sum(t_recalls)/k
    t_accuracy = sum(t_accuracys)/k

    result_dict["train_precision"] = t_precision
    result_dict["train_recall"] = t_recall
    result_dict["train_accuracy"] = t_accuracy

    return result_dict

if __name__ == '__main__':
    #data = joblib.load("tgmc_stripReal_subset.pkl")
    data = mlUtil.extract_data("nursery.csv")
    data = mlUtil.enhance_data(data)

    print k_fold_eval(data, 5)




