#!/usr/bin/env python

from digitizer import Classification, Evaluation
from digitizer import Agent as Digit_Agent
from copy import deepcopy
import math
from itertools import combinations

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
        self.top_words = top_words(20, self.word_dict())


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
class Agent(Digit_Agent):
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
        self.most_confusing_evaluations = []

        # Generate classes and word_dict from test messages
        self.generate_training_data(training_file)
        self.test_messages = get_messages(test_file)
        self.classify_messages()
        self.evaluate_classifications()
        self.set_most_confusing_evaluations()

    def whole_shebang(self):
        """c
        """
        print "The Confusion Matrix:================================="
        self.print_confusion_matrix()
        print "======================================================"
        print "The Top 20 Words per Class:==========================="
        self.print_top_20_words()
        print "======================================================"
        print "The Odds:============================================="
        self.print_odds()
        print "======================================================"


    def set_most_confusing_evaluations(self):
        """c
        """
        evaluations = []
        confusion_matrix = self.confusion_matrix
        while len(classifications) < 4:
            success_rate = 100.0
            most_confusing_evaluation = ""
            for key in confusion_matrix:
                if key not in evaluations:
                    evaluation = confusion_matrix[key]
                    e_success_rate = evaluation.get_MAP_success_rate()
                    if e_success_rate < success_rate:
                        success_rate = e_success_rate
                        most_confusing_evaluation = key
            evaluations.append(key)
        self.most_confusing_evaluations = evaluations


    def print_top_20_words(self):
        """c
        """
        classes = self.classes
        for aClass in classes:
            top_dict = aClass.top_words
            print "%s: Top 20 Words" %(aClass.alias)
            for word in top_dict:
                count = top_dict[word]
                print "\t%10s\t%5d" %(word, count)

    def print_odds(self):
        """c
        """
        classes = self.classes
        most_confusing_combos = combinations(
            self.most_confusing_evaluations,
            2
        )
        for combo in most_confusing_combos:
            print "##################################################"
            id1 = combo[0]
            id2 = combo[1]
            class_1 = classes[id1]
            class_2 = classes[id2]
            print "%s and %s" %(class_1.alias, class_2.alias)
            twenty_odds = top_odds(class_1, class_2)
            for word in twenty_odds:
                word_odd = twenty_odds[word]
                msg = "\t%s\t%.5f" %(word, word_odd)
                if word_odd < 0:
                    msg = color_text(msg, "cyan")
                elif word_odd > 0:
                    msg = color_text(msg, "red")
                else:
                    msg = color_text(msg, "yellow")
                print msg


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
                for key in classes:
                    pwgc = p_of_word_given_class(
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


def top_words(num, aDict):
    """c
    """
    num = int(num)
    if num < 0:
        num = 0
    top = []
    top_dict = {}
    word_dict = aDict
    while len(top) < num:
        most_common_count = 0
        most_common_word = ""
        for word in word_dict:
            count = word_dict[word]
            if word not in top:
                if count > most_common_count:
                    most_common_word = word
                    most_common_count = count
        top.append(most_common_word)
        top_dict[most_common_word] = count
    return top_dict


def log(num):
    """c
    """
    if num == 0:
        return -100
    else:
        return math.log(num)

def p_of_word_given_class(word, aClass):
    """c
    """
    word_count = aClass.word_count
    word_dict = aClass.word_dict
    return p_of_word(word, word_dict, word_count)

def odds(word, class_1, class_2):
    """c
    """
    pwgc1 = p_of_word_given_class(word, class_1)
    pwgc2 = p_of_word_given_class(word, class_2)
    if pwgc2 == 0:
        return 0.0
    return log(pwgc1/pwgc2)

def top_odds(class_1, class_2):
    """c
    """
    words_checked = {}
    top_words1 = class_1.top_words
    top_words2 = class_2.top_words
    for word in top_words1:
        the_odds = odds(word, class_1, class_2)
        words_checked[word] = the_odds
    for word in top_words2:
        if word not in words_checked:
            the_odds = odds(word, class_1, class_2)
            words_checked[word] = the_odds
    return words_checked








