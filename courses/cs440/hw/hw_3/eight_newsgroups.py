#!/usr/bin/env python

from digitizer import Classification, Evaluation
import digitizer
from copy import deepcopy
import math

CLASSMAP = {
    '0': 'sci.space',
    '1': 'comp.sys.ibm.pc.hardware',
    '2': 'rec.sport.baseball',
    '3': 'comp.windows.x',
    '4': 'talk.politics.misc',
    '5': 'misc.forsale',
    '6': 'rec.sport.hockey',
    '7': 'comp.graphics'
}

# P of word laplace
PWL = 10.0

# P of class laplace
PCL = 5.0
# P of class laplace V
PCLV = len(CLASSMAP)


class Message(object):
    """c
    """
    def __init__(self, data_line):
        """c
        """
        self.classification = None
        #-------------------------------------------------------------
        # Generated and stored data
        word_dict = {}
        label = ''
        #-------------------------------------------------------------
        # Store label for later comparison
        label = data_line[0]
        data_line = data_line[1:]

        for i in range(len(data_line)):
            data_line[i] = data_line[i].split(':')
            data = data_line[i]
            word = data[0]
            count =  int(data[1])
            if word in word_dict:
                word_dict[word] += count
            else:
                word_dict[word] = count

        self.word_dict = word_dict
        self.label = label
        self.word_count = sum(word_dict.values())




class Class(object):
    """c
    """
    def __init__(self, label, messages):
        """c
        """
        # Label not needed, as Class objects are organized by Agent
        # object
        # training_messages used to generate stats, not set as an
        # instance member
        self.label = label
        self.alias = CLASSMAP[label]
        self.count = len(messages)
        self.word_dict = self.get_words(messages)
        self.word_count = sum(self.word_dict.values())


    def get_words(self, messages):
        """c
        """
        word_dict = {}
        for message in messages:
            mDict = message.word_dict
            for word in mDict:
                if word in word_dict:
                    word_dict[word] += mDict[word]
                else:
                    word_dict[word] = mDict[word]
        return word_dict



# ORDER OF EXECUTION
#   __init__
#   classify_messages()
#   confusion_matrix = evaluate_message_classifications()
#   print
class Agent(digitizer.Agent):
    """c
    """
    def __init__(self, training_file, test_file):
        """c
        """
        self.test_messages = []

        self.word_dict = {}
        self.message_count = 0
        self.word_count = 0
        self.classes = {}
        self.confusion_matrix = {}

        # Generate classes and word_dict from test messages
        self.generate_training_data(training_file)
        self.test_messages = get_messages(test_file)
        self.classify_messages()
        self.evaluate_classifications()

    def whole_shebang(self):
        """c
        """
        print "The Confusion Matrix:================================="
        self.print_confusion_matrix()
        print "======================================================"


    def generate_training_data(self, training_file):
        """c
        """
        word_dict = {}
        classes = {}
        message_count = 0

        messages = get_messages(training_file)
        message_count = len(messages)

        for message in messages:
            label = message.label
            if label in classes:
                classes[label].append(message)
            else:
                classes[label] = [message]

            words = message.word_dict
            for word in words:
                if word in word_dict:
                    word_dict[word] += words[word]
                else:
                    word_dict[word] = words[word]

        for key in classes:
            classes[key] = Class(key, classes[key])

        self.classes = classes
        self.word_dict = word_dict
        self.word_count = sum(word_dict.values())
        self.message_count = message_count


    def word_in_all_classes(self, word):
        """c
        """
        in_all = True
        classes = self.classes
        for key in classes:
            word_dict = classes[key].word_dict
            if word not in word_dict:
                in_all = False
                break
        return in_all


    def classify_messages(self):
        """c
        """
        messages = self.test_messages
        classes = self.classes

        for message in messages:
            MAP_values = deepcopy(CLASSMAP)
            ML_values = deepcopy(CLASSMAP)
            for key in MAP_values:
                aClass = classes[key]
                P_aClass = log(self.p_of_class(aClass))
                MAP_values[key] = P_aClass
                ML_values[key] = 0
            word_dict = message.word_dict
            for word in word_dict:
#                if self.word_in_all_classes(word):
                for key in classes:
                    pwgc = self.p_of_word_given_class(
                        word,
                        classes[key]
                    )
                    MAP_values[key] += log(pwgc)
                    ML_values[key] += log(pwgc)
            message.classification =\
                Classification(MAP_values, ML_values)

    def evaluate_classifications(self):
        """c
        """
        evaluations = deepcopy(CLASSMAP)
        for key in evaluations:
            evaluations[key] = Evaluation()
        messages = self.test_messages
        for i in range(len(messages)):
            message = messages[i]
            label = message.label
            evaluation = evaluations[label]
            classification = message.classification
            MAP_value = classification.MAP.decision["value"]
            ML_value = classification.ML.decision["value"]
            if MAP_value == label:
                evaluation.MAP_correct.append(i)
            else:
                evaluation.MAP_incorrect.append(i)
            if ML_value == label:
                evaluation.ML_correct.append(i)
            else:
                evaluation.ML_incorrect.append(i)
        self.confusion_matrix = evaluations


    def p_of_word_given_class(
            self,
            word,
            aClass):
        """c
        """
        word_count = aClass.word_count
        word_dict = aClass.word_dict
        return p_of_word(word, word_dict, word_count)


    def p_of_class(
            self,
            aClass,
            smoothing=PCL,
            v=PCLV):
        """c
        """
        class_count = aClass.count
        message_count = self.message_count
        return ratio(
            class_count,
            message_count,
            smoothing,
            v
        )

#=====================================================================
# Utils
#---------------------------------------------------------------------


def get_messages(filename):
    """c
    """
    f = open(filename, 'r')
    array = f.read().splitlines()
    f.close()

    messages = []

    for line in range(len(array)):
        array[line] = array[line].split(' ')
        message = Message(array[line])
        messages.append(message)
    return messages


def ratio(numerator, denominator, smoothing=0.0, v=1.0):
    """c
    """
    smoothing = float(smoothing)
    v = float(v)
    numerator = (float(numerator) + smoothing)
    denominator = (float(denominator) + (smoothing * v))
    if denominator == 0:
        return 0
    return numerator / denominator


def p_of_word(word, aDict, word_count, smoothing=PWL):
    """c
    """
    try:
        count = aDict[word]
    except KeyError:
        return 0.0
    v = len(aDict)
    return ratio(
        count,
        word_count,
        smoothing,
        v
    )

def log(num):
    """c
    """
    if num == 0:
        return -100
    else:
        return math.log(num)

