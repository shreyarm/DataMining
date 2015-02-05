__author__ = 'cindi'

import csv
import sys
import numpy as np
import inspect


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def any_float(in_list):
    '''
    Are any of the elements of in_list floats?
    '''
    for i in in_list:
        if is_int(i):
            continue
        if is_float(i):
            return True
    return False


def cvrt_to_num_if_can(str, prefer_float=False):
    ''' If str is really a number,
    convert it to same, preferring floats if flag is True,
    else prefering ints
    '''

    if prefer_float and is_float(str):
        return float(str)
    if is_int(str):
        return int(str)
    if is_float(str):
        return float(str)
    return str


def cnvrt_list_to_nums(in_list):
    result = []
    for i in in_list:
        result.append(cvrt_to_num_if_can(i))


#extract data from the IBM contest training or evaluation files
def extract_ibm_data(fileName, test_file=False):
    ''' Inputs: Name of the file
    test_file: if True, we will not look for the target value, since it is not included
    Returns: a dictionary with keys 'target_names', 'target', 'q_id' and 'data'
    '''
    try:
        in_file = open(fileName, 'rU')
        s = in_file.read()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #split by line
    rows = s.strip().split("\n")
    #initialization
    datadict = {'target_names': ['true', 'false'], 'target': [], 'data': [], 'q_id': [], 'id': []}
    for row in rows:
        cols = row.split(',')
        if not test_file:
            #target classes are in last column
            datadict['target'].append(cols[-1])
            #take out target value
            cols = cols[:-1]
        #example ID in first column
        datadict['id'].append(cols[0])
        #question ID is in second column; reading in makes it a float but we want ints
        datadict['q_id'].append(int(float(cols[1])))
        #now we don't need question ID; also remove the first col, which is just an example ID
        cols = cols[2:]
        row_data = [cvrt_to_num_if_can(c) for c in cols]
        datadict['data'].append(row_data)

    return datadict


#extract data from a CSV file
def extract_data(fileName, targetInfo=None, delim =',', headers=True):
    '''Inputs: the name of a file,
    targetInfo: if None then the last column is the target variable, otherwise, it's
       either the column name (if headers) or number, if no headers.
    delim: optionally the column deliminator (',' is the default)

    Return a sklearn-style dictionary
    '''
    try:
        in_file = open(fileName, 'rUb')
        reader = csv.reader(in_file, delimiter=delim, quotechar='"')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    except ValueError:
        print "Could not convert data."
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #initialization
    dataDict = {'feature_names': [], 'target_names': [], 'target': [], 'data': []}
    fieldNames = []
    if headers:
        targetName = targetInfo
        len_row = 0
        #read the header row
        for row in reader:
            len_row = len(row)
            for field in row:
                if field != '':
                    fieldNames.append(field)
            break
        #find the index of the target value, if exists
        if targetName is not None:
            try:
                targetIdx = fieldNames.index(targetName)
            except ValueError:
                print "Target %s not in fields %s" %(targetName, fieldNames)
                raise
        else:
            targetIdx = len_row - 1

        fieldNames = fieldNames[:targetIdx] + fieldNames[targetIdx+1:]
        dataDict['feature_names'] = fieldNames

        #read the data
        for row in reader:
            #We may want to later have more sophistication if values are missing,
            # but for now we fill the example with "None"
            rowData = [None for i in range(len(fieldNames))]
            #add one to length because the target is also there
            if len(row) != len(fieldNames)+1:
                print "found a bad row? ",row
            dataIdx = 0
            for colIdx in range(len(row)):
                if colIdx == targetIdx:
                    tVal = cvrt_to_num_if_can(row[colIdx])
                    dataDict['target'].append(tVal)
                elif row[colIdx] != r'\N' and row[colIdx] != "":
                    rowData[dataIdx] = cvrt_to_num_if_can(row[colIdx])
                    dataIdx += 1
            dataDict['data'].append(rowData)
    else: #no headers
        for row in reader:
            rowData = []
            if targetInfo is None:
                #assume the target is in the last column
                targetInfo = len(row)-1
            for colIdx in range(len(row)):
                val = cvrt_to_num_if_can(row[colIdx])
                ## For decision tree data (student's version) val = row[colIdx]
                if colIdx == targetInfo:
                    dataDict['target'].append(val)
                else:
                    rowData.append(val)
            dataDict['data'].append(rowData)
        first_ex = dataDict['data'][0]
        #make the feature names just string versions of the column index of the feature
        dataDict['feature_names'] = [str(y) for y in range(len(first_ex)+1) if y != targetInfo]

    #get unique targets
    dataDict['target_names'] = list(set(dataDict['target']))
    return dataDict

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(1)


def sign(x):
    """
    Returns 1 or -1 depending on the sign of x
    """
    if x >= 0:
        return 1
    else:
        return -1


#Add new key to dictionary 'feature_dict', described further below
def enhance_data(datadict):
    ''' Return the same datadictionary as passed in, but with a new key:
        feature_dict: {a1: [a1vals], a2: [a2vals],...,ad: [advals]}
                where the dictionary keys are attribute names and the dictionary values are
                a list of all possible values for the attribute.
                Instead of a list of attribute vals, the value might be a string 'real'
                for real-valued attributes
    '''
    attribs = datadict['feature_names']
    temp_dict = {} # for attrib names -> value maps
    for i in attribs:
        temp_dict[i] = []

    for x in datadict['data']:
        for a, val in zip(attribs, x):
            #all values for the attribute
            temp_dict[a].append(val)

    #now simplify the temp dictionary
    for k, v in temp_dict.items():
        #print k,v
        vals = set(v)
        #if there are 10 or fewer values and they are not float, keep to treat as categorical feature
        #even if int
        if 0 < len(vals) <= 10 and not any_float(vals):
            temp_dict[k] = list(vals) #change it back to a list for mutability
            continue
        #if there are floats or ints, don't keep all the vals
        if any_float(vals) or all_ints(vals):
            temp_dict[k] = 'numeric'
            continue
        #else
        temp_dict[k] = list(vals)

    datadict['feature_dict'] = temp_dict
    return datadict


def all_ints(in_list):
    '''
    Are all the elements of in_list integers?
    '''
    for i in in_list:
        if not is_int(i):
            return False
    return True


def score(model, X, y):
    '''
    Similar to the score methods of sklearn. For you to modify and
    use as a helper method for cross-validation.
    Prints and returns raw model accuracy over a dataset
    '''
    predictions = model.predict(X)
    num_right = 0.0
    num_exs = len(X)
    for i in range(num_exs):
        if predictions[i]== y[i]:
            num_right += 1

    result = num_right/num_exs
    print 'Test set accuracy: %f' % result
    return result


class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend