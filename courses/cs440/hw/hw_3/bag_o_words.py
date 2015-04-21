#!/usr/bin/env python

from digitizer import Agent as Digit_Agent
from copy import deepcopy
from hw_3_utils import color_text, get_color_index, log, ratio
from hw_3_utils import Classification, Evaluation
import sys

CLASSMAP8 = {
    '0': 'sci.space',
    '1': 'comp.sys.ibm.pc.hardware',
    '2': 'rec.sport.baseball',
    '3': 'comp.windows.x',
    '4': 'talk.politics.misc',
    '5': 'misc.forsale',
    '6': 'rec.sport.hockey',
    '7': 'comp.graphics'
}

CLASSMAPSPAM = {
    '0': "mail",
    '1': "spam"
}

# P of word laplace
PWL = 10.0

# P of class laplace
PCL = 5.0


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
    def __init__(self, label, messages, agent_type):
        """c
        """
        # Label not needed, as Class objects are organized by Agent
        # object
        # training_messages used to generate stats, not set as an
        # instance member
        self.label = label
        if agent_type == "spam":
            self.alias = CLASSMAPSPAM[label]
        else:
            self.alias = CLASSMAP8[label]
        self.count = len(messages)
        self.word_dict = self.get_words(messages)
        self.word_count = sum(self.word_dict.values())
        self.top_words = top_words(20, self.word_dict)


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
    def __init__(self, training_file, test_file, agent_type):
        """c
        """
        self.agent_type = agent_type
        self.test_messages = []
        self.confusion_matrix = self.base_confusion_matrix()

        self.word_dict = {}
        self.message_count = 0
        self.word_count = 0
        self.classes = {}
        self.classification_table = {}
        self.most_confusing_evaluations = []

        # Generate classes and word_dict from test messages
        self.generate_training_data(training_file)
        self.test_messages = get_messages(test_file)
        self.classify_messages()
        self.evaluate_classifications()
        self.generate_most_confusing(4)

    def print_confusion_matrix(self):
        """c
        """
        matrix = self.confusion_matrix
        msg = ' ' * 4
        map_dict = CLASSMAP8
        if self.agent_type == "spam":
            map_dict = CLASSMAPSPAM
        for i in range(len(map_dict)):
            msg += "%4d" %(i)
        msg += '\n'
        msg += ('-' * 4 * len(map_dict))
        msg += ('-' * 4)
        for i in range(len(matrix)):
            msg += '\n'
            msg += '%3d|' %(i)
            for j in range(len(matrix[i])):
                if i == j:
                    value = '_'
                    msg += "%4s" %(value)
                else:
                    value = matrix[i][j]
                    msg += "%4d" %(value)
        print msg

    def base_confusion_matrix(self):
        """c
        """
        matrix = []
        map_dict = CLASSMAP8
        if self.agent_type == "spam":
            map_dict = CLASSMAPSPAM
        for i in range(len(map_dict)):
            matrix.append([])
            for _ in range(len(map_dict)):
                matrix[i].append(0)
        return matrix

    def whole_shebang(self):
        """c
        """
        print "The Classification Methods Comparison Table:=========="
        self.print_classification_table()
        print "======================================================"
        print "The Confusion Matrix:================================="
        self.print_confusion_matrix()
        print "======================================================"
        print "The Top 20 Words per Class:==========================="
        self.print_top_20_words()
        print "======================================================"
        print "The Top 20 Odds Ratios for Confusing Messages:========"
        self.print_odds()
        print "======================================================"


    def generate_most_confusing(self, num):
        """c
        """
        most_confusing = []
        matrix = self.confusion_matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if i == j:
                    continue
                count = matrix[i][j]
                item = (count, i, j)
                most_confusing.append(item)
        most_confusing.sort()
        if len(most_confusing) >= num:
            most_confusing = most_confusing[-num:]
        self.most_confusing_evaluations = most_confusing


    def print_top_20_words(self):
        """c
        """
        classes = self.classes
        for key in classes:
            aClass = classes[key]
            top_dict = aClass.top_words
            print "%s: Top 20 Words" %(aClass.alias)
            for word in top_dict:
                count = top_dict[word]
                print "\t%-25s\t%5d" %(word, count)

    def print_odds(self):
        """c
        """
        classes = self.classes
        most_confusing = self.most_confusing_evaluations
        for combo in most_confusing:
            print "##################################################"
            _, id1, id2 = combo
            class_1 = classes[str(id1)]
            class_2 = classes[str(id2)]
            print "%s and %s" %(class_1.alias, class_2.alias)
            twenty_odds, min_odd, max_odd = top_odds(class_1, class_2)
            print "Range: %.5f --> %.5f" %(min_odd, max_odd)
            print "--------------------------------------------------"
            for word in twenty_odds:
                word_odd = twenty_odds[word]
                msg = "\t%-15s%6.5f" %(word, word_odd)
                index = get_color_index(word_odd, min_odd, max_odd)
                index = max(index, 1)
                msg = color_text(msg, index, "black")
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
            classes[key] = Class(key, classes[key], self.agent_type)

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
            if self.agent_type == "spam":
                to_copy = CLASSMAPSPAM
            else:
                to_copy = CLASSMAP8
            MAP_values = deepcopy(to_copy)
            ML_values = deepcopy(to_copy)
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
        if self.agent_type == "spam":
            to_copy = CLASSMAPSPAM
        else:
            to_copy = CLASSMAP8
        evaluations = deepcopy(to_copy)
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
                self.confusion_matrix[int(label)][int(MAP_value)] += 1
            if ML_value == label:
                evaluation.ML_correct.append(i)
            else:
                evaluation.ML_incorrect.append(i)
        self.classification_table = evaluations


    def p_of_class(
            self,
            aClass,
            smoothing=PCL):
        """c
        """
        class_count = aClass.count
        message_count = self.message_count
        if self.agent_type == "spam":
            v = len(CLASSMAPSPAM)
        else:
            v = len(CLASSMAP8)
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
        top_dict[most_common_word] = most_common_count
    return top_dict


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
    return log(ratio(pwgc1, pwgc2))

def top_odds(class_1, class_2):
    """c
    """
    common_words = {}
    top_words1 = class_1.word_dict
    top_words2 = class_2.word_dict
    the_20_top_odds = {}
    for word in top_words1:
        if word not in top_words2:
            continue
        the_odds = odds(word, class_1, class_2)
        common_words[word] = the_odds
    while len(the_20_top_odds) < 20:
        max_odds = -sys.maxint - 1
        the_word = ""
        for word in common_words:
            if word in the_20_top_odds:
                continue
            the_odds = common_words[word]
            if the_odds > max_odds:
                max_odds = the_odds
                the_word = word
        the_20_top_odds[the_word] = max_odds
    min_odds = min(the_20_top_odds.values())
    max_odds = max(the_20_top_odds.values())
    return the_20_top_odds, min_odds, max_odds

