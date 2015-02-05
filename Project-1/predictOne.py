import util
import classificationMethod

class predictOne(classificationMethod.ClassificationMethod):
    """
    This defines the classifier that always predicts +1.
    """
    def __init__(self, legalLabels):
        self.guess = None
        self.type = "allOnes"

    def train(self, data, labels, validationData, validationLabels):
        """ do nothing"""

    def classify(self, testData):
        return [1]*len(testData)  # return our constant prediction
