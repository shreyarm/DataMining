from sklearn.externals import joblib
import mlUtil
from math import log as log
import argparse

#helper method & sample solution for ZeroR fit method
def zeroR(data):
    '''
       Given a list or sklearn-style dictionary, return the most common value
    '''
    if type(data) == dict:
        y_vals = data['target']
    else:
        y_vals = data
    class_counts = dict.fromkeys(y_vals, 0)
    for i in y_vals:
        class_counts[i] += 1
    return max(class_counts, key=class_counts.get)


class DecisionTree():
    '''
    Sklearn-style decision tree classifier, using entropy
    '''
    def __init__(self, attrib_d=None, attribs=None, default_v=None):
        ''' initialize classifier
        '''
        if not attribs:
            attribs = []
        if attrib_d:
            self.attrib_dict = attrib_d
        else:
            attrib_d = {}
            self.attrib_dict = attrib_d
        self.attribute_list = attribs
        self.default_value = default_v
        
        "*** YOUR CODE HERE AS NEEDED ***"
        self.clf = None


    def fit(self, X, y):
        '''X and y are as in sklearn classifier.fit expected arguments
        Creates a decision tree
        '''
        "*** YOUR CODE HERE AS NEEDED***"

        attributes = self.attribute_list[:]
        self.clf = self.makeTree(X, y, attributes, self.attrib_dict, self.default_value)
        return self.clf

    def predict(self, X):
        ''' Return a class label using the decision tree created by the fit method
        '''
        "*** YOUR CODE HERE AS NEEDED***"
        #call recursive classify method on the learned tree for each x in X
        value = []
        attribute = self.clf.attribute
        children = self.clf.children
        for x in X:
         self.clf.attribute = attribute
         self.clf.children = children
         value.append(self.clf.classify(x,self.attribute_list,self.default_value))
        return value

    def entropy(self, labels):
        '''takes as input a list of class labels. Returns a float
        indicating the entropy in this data.
        Hint: you don't have to implement log_2(x), see math.log()
        '''
        total_entropy = 0.0;
        target_dict = dict([(target, list(labels).count(target)) for target in set(labels)])
        for target in target_dict:
            tar_count = target_dict[target]
            p = tar_count/float(len(labels))
            total_entropy = -(p*log(p,2)) + total_entropy
        return total_entropy

    ### Compute remainder - this is the amount of entropy left in the data after
    ### we split on a particular attribute. Let's assume the input data is of
    ### the form:
    ###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
    def remainder(self, data) :
        possibleValues = set([item[0] for item in data])
        r = 0.0
        for value in possibleValues :
            c = [item[0] for item in data].count(value)
            r += (float(c) / len(data) ) * self.entropy([item[1] for item in
                                                data if item[0] == value])
        return r

    ###
    def selectAttribute(self, X, y):
        '''
        selectAttribute: choose the index of the attribute in the current
        dataset that minimizes remainder(A).
        '''
        remainders = []
        if len(X[0]) == 1:
          return 0;
        for i in range(len(X[0])-1):
            data = []
            for x in X:
                feature = x[i]
                target = y[X.index(x)]
                data.append((feature,target))
            remainders.append(self.remainder(data))
        return remainders.index(min(remainders))

    ### a tree is simply a data structure composed of nodes (of type TreeNode).
    ### The root of the tree
    ### is itself a node, so we don't need a separate 'Tree' class. We
    ### just need a function that takes in a dataset and our attribute dictionary,
    ### builds a tree, and returns the root node.
    ### makeTree is a recursive function. Our base case is that our
    ### dataset has entropy 0 - no further tests have to be made. There
    ### are two other degenerate base cases: when there is no more data to
    ### use, and when we have no data for a particular value. In this case
    ### we use either default value or majority value.
    ### The recursive step is to select the attribute that most increases
    ### the gain and split on that.
    ### assume: input looks like this:
    ### dataset: [[v11, v21, ..., vd1], [v12,v22, ..., vd2] ...[v1n,v2n,...vdn] ],
    ###    remaining training examples with values for only the unused features
    ### labels: [c1, ..., cn], remaining target labels for the dataset
    ### attributes: [a1, a2, ...,ax] the list of remaining attribute names
    ### attrib_dict: {a1: [a1vals], a2: [a2vals],...,ad: [advals]}
    ### the dictionary keys are attribute names and the dictionary values are either the list
    ### of values that attribute takes on or 'real' for real-valued attributes (handle for Extra Credit)
    def makeTree(self, dataset = None, labels = None, attributes = None, attrib_dict = None, defaultValue = None):
        ''' Helper recursive function for creating a tree
        '''
        "*** YOUR CODE HERE ***"
        if not dataset:
            leaf = TreeNode(value=defaultValue)
            return leaf

        if self.entropy(labels) == 0.0:
           leaf = TreeNode(value=labels[0])
           return leaf

        if len(attributes)==0:
            major_value = zeroR(labels)
            leaf = TreeNode(value=major_value)
            return leaf

        split_index = self.selectAttribute(dataset,labels)

        attribute = attributes[split_index]
        feat_vals = set([data[split_index] for data in dataset])
        node = TreeNode(attribute=attribute)
        attributes.pop(split_index)
        for value in feat_vals:
          subset = []
          sublabels = []
          sub_attributes = []
          for data in dataset:
              if data[split_index] == value:
                sub_attributes = attributes[:]
                subdata = data[:split_index]
                subdata.extend(data[split_index+1:])
                subset.append(subdata)
                sublabels.append(labels[dataset.index(data)])
          node.children[value] = self.makeTree(subset,sublabels,sub_attributes,attrib_dict,defaultValue)
        return node

### Helper class for DecisionTree.
### A TreeNode is an object that has either:
### 1. An attribute to be tested and a set of children, one for each possible
### value of the attribute, OR
### 2. A value (if it is a leaf in a tree)
class TreeNode:
    def __init__(self, attribute = None, value = None):
        self.attribute = attribute
        self.value = value
        self.children = {}

    def __repr__(self):
        if self.attribute:
            return self.attribute
        else:
            return self.value

    ### a node with no children is a leaf
    def is_leaf(self):
        return self.children == {}

    ###
    def classify(self, x, attributes, default_value):
       '''
       return the value for the given data
       the input will be:
       x - an object to classify - [v1, v2, ..., vn]
        attributes - the names of all the attributes
       '''
       "*** YOUR CODE HERE ***"
       if self.is_leaf():
           return self.value
       else:
         node = self.attribute
         children_dict = self.children
         att_index = attributes.index(node)
         a_val = x[att_index]

         if a_val in children_dict:
           children = children_dict[a_val]
         else:
          return default_value
         if children:
              if children.is_leaf():
                  return children.value
              else:
                  self.attribute = children.attribute
                  self.children = children.children
                  return self.classify(x,attributes,default_value)
         else:
             return default_value



#here's a way to visually check your tree
def printTree(root, val='Tree', indentNum=0):
    """ For printing the decision tree in a nice format
        Usage: printTree(rootNode)
    """
    indent = "\t"*indentNum
    if root.is_leaf():
        print indent+"+-"+str(val)+'-- '+root.value

    else:
        print indent+"+-"+str(val)+'-- <'+root.attribute+'>'
        print indent+"{"
        for k in root.children.keys():
            printTree(root.children[k],k,indentNum+1)
        print indent+"}"



if __name__ == '__main__':
    #parse the command line arguments

    data = mlUtil.extract_data("lymphography.csv")
    data = mlUtil.enhance_data(data)

    tree = DecisionTree(attrib_d = data['feature_dict'], attribs = data['feature_names'],default_v="default")
    tree.fit(data['data'], data['target'])
    printTree(tree.clf)
    #test on training data
    print data['target']
    print tree.predict(data['data'])

