__author__ = 'cindi'
import unittest
import decisionTree
import mlUtil as mu
import inspect


class TestTreeBuilder(unittest.TestCase):
    """
    P1 testing code
    """

    def testEntropyEmpty(self):
        """
        Test with empty list
        """
        dt = decisionTree.DecisionTree()
        self.assertEquals(dt.entropy([]), 0)

    def testEntropyOneEl(self):
        """
        Test with all same element, empty list,  more than 2 labels,
        and a couple uneven distributions
        """
        dt = decisionTree.DecisionTree()
        self.assertEquals(dt.entropy(['yes']), 0)

    def testEntropyAllSame(self):
        dt = decisionTree.DecisionTree()
        self.assertEquals(dt.entropy(['yes','yes']), 0)

    def testEntropyMax(self):
        dt = decisionTree.DecisionTree()
        self.assertEquals(dt.entropy(['yes','no']), 1.0)

    def testEntropyThreeVal(self):
        dt = decisionTree.DecisionTree()
        self.assertAlmostEquals(dt.entropy(['yes','no','maybe']), 1.58496, places=4)

    def testEntropyUnbal(self):
        dt = decisionTree.DecisionTree()
        self.assertAlmostEquals(dt.entropy(['yes','no','yes']), 0.918296, places=4)

    def testSelAttTenn(self):
        dt = decisionTree.DecisionTree()
        tennis = mu.extract_data('tennis.csv')
        attrib = dt.selectAttribute(tennis['data'], tennis['target'])
        self.assertEquals(attrib, 0)

    def testSelAttRest(self):
        dt = decisionTree.DecisionTree()
        rest = mu.extract_data('restaurant.csv')
        attrib = dt.selectAttribute(rest['data'], rest['target'])
        self.assertEquals(attrib, 4)

    def testbuildZeroEnt(self):
        dt = decisionTree.DecisionTree()
        tree = dt.makeTree([[1,'a'],[2,'a']], ['yes','yes'],['a1','a2'],
                           {'a1': [1,2], 'a2': ['a','b']}, 'default')
        self.assertEquals(repr(tree), 'yes')

    def testbuildEmpty(self):
        dt = decisionTree.DecisionTree()
        tree = dt.makeTree([],[],[],{},'default')
        self.assertEquals(repr(tree), 'default')

    def testOneFeature(self):
        dt = decisionTree.DecisionTree()
        tree = dt.makeTree([[1],[1],[2]], ['no','yes','yes'], ['a1'],
                           {'a1': [1,2], 'a2': ['a','b']}, 'default')
        self.assertEquals(tree.attribute, 'a1')

    def testNoFeatures(self):
        dt = decisionTree.DecisionTree()
        tree = dt.makeTree([[],[],[]], ['no','yes','yes'], [],
                           {'a1': [1,2], 'a2': ['a','b']}, 'default')
        self.assertEquals(repr(tree), 'yes')


    def testRecursiveBuild(self):
        dt = decisionTree.DecisionTree()
        tree = dt.makeTree([[1,'a'],[2,'a']], ['yes','no'],['a1','a2'],
                           {'a1': [1,2], 'a2': ['a','b']}, 'default')
        self.assertNotEquals(repr(tree), 'yes')
        self.assertNotEquals(repr(tree), 'no')
        self.assertNotEquals(repr(tree), 'default')

    def testFitEmpty(self):
        dt = decisionTree.DecisionTree(default_v='default')
        dt.fit([],[])
        self.assertEquals(repr(dt.clf), 'default')

    def testPredict(self):
        """
        build the tree node for test
            attr1
         +----+--------+
        v1   v2       v3
         |    |        |
        foo  bar     attr2
                     +-+-+
                    v4  v5
                     |   |
                    boo far

        """
        v4 = decisionTree.TreeNode("","boo")
        v5 = decisionTree.TreeNode("","far")
        attr2 = decisionTree.TreeNode("attr2",None)
        attr2.children = {'v4': v4, 'v5': v5}
        root = decisionTree.TreeNode('attr1',None)
        root.children = {'v1': decisionTree.TreeNode('','foo'),
                         'v2': decisionTree.TreeNode('','bar'),
                         'v3': attr2}
        a_d = ['attr1','attr2']
        self.assertEquals(root.classify(['v1','v4'], a_d, 'def'), 'foo')
        self.assertEquals(root.classify(['v2','v5'], a_d, 'def'), 'bar')
        self.assertEquals(root.classify(['v3', 'v4'], a_d, 'def'), 'boo')
        self.assertEquals(root.classify(['v3', 'v5'], a_d, 'def'), 'far')

    def testPredictDefault(self):
        v4 = decisionTree.TreeNode("","boo")
        v5 = decisionTree.TreeNode("","far")
        attr2 = decisionTree.TreeNode("attr2",None)
        attr2.children = {'v4': v4, 'v5': v5}
        root = decisionTree.TreeNode('attr1',None)
        root.children = {'v1': decisionTree.TreeNode('','foo'),
                         'v2': decisionTree.TreeNode('','bar'),
                         'v3': attr2}
        a_d = ['attr1','attr2']
        self.assertEquals(root.classify(['v4','v1'], a_d, 'def'), 'def')
        self.assertEquals(root.classify(['v3','v1'], a_d, 'def'), 'def')

    def testTennis(self):
        """
        Test entire program on the tennis data set
        """
        tennis = mu.extract_data('tennis.csv')
        tennis = mu.enhance_data(tennis)
        dt = decisionTree.DecisionTree(tennis['feature_dict'], tennis['feature_names'])
        dt.fit(tennis['data'],tennis['target'])
        for x,y in zip(tennis['data'],tennis['target']):
            self.assertEquals(dt.predict([x]), [y])
        self.assertEquals(dt.predict(tennis['data']), tennis['target'])


if __name__ == '__main__' :
    print "running tests"
    unittest.main()