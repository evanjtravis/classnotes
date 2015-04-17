#!/usr/bin/env python

from digitizer import Classification, Evaluation
import digitizer


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

LAPLACE = 0.0


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
        word_count = 0
        #-------------------------------------------------------------
        # Store label for later comparison
        label = data_line[0]
        data_line = data_line[1:]

        for i in range(len(data_line)):
            data_line[i] = data_line[i].split(':')
            data = data_line[i]
            word = data[0]
            count =  data[1]
            if word in word_dict:
                word_dict[word] += count
            else:
                word_dict[word] = count

        self.word_dict = word_dict
        self.label = label
        self.word_count = sum(word_dict.values())



class Word(object):
    """c
    """
    def __init__(self, text):
        """c
        """
        self.text = text

    def p_of_word_given_class(self, message_class):
        """c
        """
        pass



class MessageClass(object):
    """c
    """
    def __init__(self, label, training_messages):
        """c
        """
        # training_messages used to generate stats, not set as an
        # instance member
        self.label = label
        self.alias = CLASSMAP[label]

        self.p, class_messages =\
            self.get_probability(training_messages)
        self.word_dict = get_word_dict(messages)





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
        self.training_messages = []
        self.test_messages = []
        self.training_words = {}
        self.confusion_matrix = {}

        self.training_messages = get_messages(training_file)
        self.words = self.get_words()
        self.classes = self.get_classes()

        self.test_messages = get_messages(test_file)


    def get_words(self):
        """c
        """
        pass


#=====================================================================
# Utils
#---------------------------------------------------------------------
def p_of_word(word, word_dict, smoothing=0.0, v=0.0):
    """c
    """
    try:
        word_count = word_dict[word]
    except KeyError:
        return 0.0
    total_word_count = sum(word_dict.values())

    return ratio(
        word_count,
        total_word_count,
        smoothing,
        v
    )


def p_of_word_given_class(word, classStat):
    """c
    """
    pass

def p_of_class_given_word(classStat, word):
    """c
    """
    pass




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


def ratio(numerator, denominator, smoothing=0.0, v=0.0):
    """c
    """
    smoothing = float(smoothing)
    v = float(v)
    numerator = (float(numerator) + smoothing)
    denominator = (float(denominator) + (smoothing * v))
    return numerator / denominator


def get_word_dict(messages):
    """c
    """
    words = {}
    for message in messages


