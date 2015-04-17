#!/usr/bin/env python
DATA_DIR = "spam_detection/"
LAPLACE = 0.0

import os
import math
import digitizer
from digitizer import Classification, Evaluation

class Message(object):
    """c
    """
    def __init__(self, data_line):
        """c
        """
        self.classification = None # will be a classification object
        # holding labels identifying it as either spam or mail
        #-------------------------------------------------------------
        # Data to Store in Object from data_line
        word_dict = {}
        word_count = 0
        word_probabilities = {}
        label = None
        #-------------------------------------------------------------
        # Save label for evaluation
        label = data_line[0]
        data_line = data_line[1:]

        for i in range(len(data_line)):
            data_line[i] = data_line[i].split(':')
            word = data_line[i][0]
            count = int(data_line[i][1])
            if word in word_dict:
                word_dict[word] += count
            else:
                word_dict[word] = count
            word_count += count

        for word in word_dict:
            count = word_dict[word]
            word_probabilities[word] =\
                laplace_smooth(count, word_count)

        self.word_dict = word_dict
        self.word_count = word_count
        # A better name would be word_ratios
        self.word_probabilities = word_probabilities
        self.label = label



class Agent(digitizer.Agent):
    """c
    """
    def __init__(self):
        """c
        """
        self.confusion_matrix = None
        self.data = get_training_data() # Trains as well
        self.messages, self.message_count = get_test_messages()
        self.classify_messages()
        self.evaluate_classifications()

    def whole_shebang(self):
        """c
        """
        print "The Confusion Matrix:=============================="
        self.print_confusion_matrix()
        print"===================================================="


    def evaluate_classifications(self):
        """c
        """
        evaluations = {
            "mail": Evaluation(),
            "spam": Evaluation()
        }
        messages = self.messages
        for i in range(len(messages)):
            message = messages[i]
            label = message.label
            if label == '1':
                label = "spam"
            else:
                label = "mail"
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


    def classify_messages(self):
        """c
        """
        Pclass = self.data["class_probabilities"]
        Pmail = math.log(Pclass["mail"])
        Pspam = math.log(Pclass["spam"])

        messages = self.messages
        agent_Pword_dict = self.data["word_probabilities"]
        mail_Pword_dict = self.data["mail_word_probabilities"]
        spam_Pword_dict = self.data["spam_word_probabilities"]
        for message in messages:
            MAP_values = {
                "mail": Pmail,
                "spam": Pspam,
            }
            ML_values = {
                "mail": 0,
                "spam": 0
            }
            word_dict = message.word_dict
            for word in word_dict:
                # first check if word exists in either mail or spam
                if word not in agent_Pword_dict:
                    continue
                # consider words only contained in spam and mail
                # messages
                if word in mail_Pword_dict and word in spam_Pword_dict:
                    # mail
                    P_word_given_mail = math.log(mail_Pword_dict[word])
                    MAP_values["mail"] += P_word_given_mail
                    ML_values["mail"] += P_word_given_mail
                    # spam
                    P_word_given_spam = math.log(spam_Pword_dict[word])
                    MAP_values["spam"] += P_word_given_spam
                    ML_values["spam"] += P_word_given_spam
            message.classification =\
                Classification(MAP_values, ML_values)


def get_test_messages():
    """c
    """
    filename = "test_email.txt"
    path = os.path.join(DATA_DIR, filename)
    f = open(path, 'r')
    array = f.read().splitlines()
    f.close()

    messages = [] # Contain message objects
    message_count = 0

    for line in range(len(array)):
        array[line] = array[line].split(' ')
        message = Message(array[line])
        messages.append(message)
        message_count += 1
    return messages, message_count


def get_training_data():
    """c
    """
    filename = "train_email.txt"
    path = os.path.join(DATA_DIR, filename)
    f = open(path, 'r')
    array = f.read().splitlines()
    f.close()

    mail = []
    spam = []
    total_mail_count = 0
    #-----------------------------------------------------------------
    # DATA TO GENERATE AND RETURN
    mail_count = 0
    spam_count = 0

    mail_dict = {}
    spam_dict = {}

    mail_word_count = 0
    spam_word_count = 0

    class_probabilities = {
        "mail": 0,
        "spam": 0
    }
    mail_word_probabilities = {}
    spam_word_probabilities = {}

    word_count = 0
    word_dict = {}
    word_probabilities = {}
    #-----------------------------------------------------------------

    for line in range(len(array)):
        array[line] = array[line].split(' ')
        if array[line][0] == '1':
            spam.append(array[line][1:])
            spam_count += 1
        else:
            mail.append(array[line][1:])
            mail_count += 1
        total_mail_count += 1

    for i in range(len(mail)):
        for j in range(len(mail[i])):
            mail[i][j] = mail[i][j].split(':')
            word = mail[i][j][0]
            count = int(mail[i][j][1])
            if word in mail_dict:
                mail_dict[word] += count
            else:
                mail_dict[word] = count
            if word in word_dict:
                word_dict[word] += count
            else:
                word_dict[word] = count
            word_count += count
            mail_word_count += count

    for i in range(len(spam)):
        for j in range(len(spam[i])):
            spam[i][j] = spam[i][j].split(':')
            word = spam[i][j][0]
            count = int(spam[i][j][1])
            if word in spam_dict:
                spam_dict[word] += count
            else:
                spam_dict[word] = count
            if word in word_dict:
                word_dict[word] += count
            else:
                word_dict[word] = count
            word_count += count
            spam_word_count += count

    class_probabilities["spam"] =\
        laplace_smooth(spam_count, total_mail_count, 2)
    class_probabilities["mail"] =\
        laplace_smooth(spam_count, total_mail_count, 2)


    for word in mail_dict:
        count = mail_dict[word]
        mail_word_probabilities[word] =\
            laplace_smooth(count, mail_count, len(mail_dict))

    for word in spam_dict:
        count = spam_dict[word]
        spam_word_probabilities[word] =\
            laplace_smooth(count, spam_count, len(spam_dict))

    for word in word_dict:
        count = word_dict[word]
        word_probabilities[word] =\
            laplace_smooth(count, word_count, len(word_dict))

    data_dict = {
        "mail_count": mail_count,
        "spam_count": spam_count,

        "mail_dict": mail_dict,
        "spam_dict": spam_dict,

        "mail_word_count": mail_word_count,
        "spam_word_count": spam_word_count,

        "class_probabilities": class_probabilities,
        "mail_word_probabilities": mail_word_probabilities,
        "spam_word_probabilities": spam_word_probabilities,

        "word_count": word_count,
        "word_dict": word_dict,
        "word_probabilities": word_probabilities # P(word)
    }
    return data_dict

#=====================================================================
# Utils
#---------------------------------------------------------------------
def laplace_smooth(numerator, denominator, V=2.0):
    """c
    """
    V = float(V)
    numerator = (float(numerator) + LAPLACE)
    denominator = (float(denominator) + LAPLACE * V)
    return numerator / denominator

#=====================================================================
