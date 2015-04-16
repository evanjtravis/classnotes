#!/usr/bin/env python

import os
import math
from itertools import combinations

DIGITS_DIR = "digitdata/"
BLOCK_SIZE = 28

class Pixel(object):
    """c
    """
    def __init__(self, coords):
        self.coords = coords
        self.zero_count = 0
        self.one_count = 0
        self.laplace = 10.0
        self.zero_likelihood = None
        self.one_likelihood = None
        self.possible_values = 2.0

    def determine_one_likelihood(self, class_count):
        self.one_likelihood =\
            (float(self.one_count) + self.laplace) /\
            (float(class_count) + self.laplace * self.possible_values)

    def determine_zero_likelihood(self, class_count):
        self.zero_likelihood =\
            (float(self.zero_count) + self.laplace) /\
            (float(class_count) + self.laplace * self.possible_values)

class Digit(object):
    """Class
    """
    def __init__(self, digit):
        """c
        """
        self.digit = digit
        digit_pixels = []
        for i in range(BLOCK_SIZE):
            digit_pixels.append([])
            for j in range(BLOCK_SIZE):
                digit_pixels[i].append(Pixel((i,j)))
        self.pixels = digit_pixels
        self.instances = 0
        self.likelihood = 0

    def add_zero(self, coords):
        """c
        """
        x, y = coords
        self.pixels[x][y].zero_count += 1

    def add_one(self, coords):
        """c
        """
        x, y = coords
        self.pixels[x][y].one_count += 1

    def determine_pixel_likelihoods(self):
        """c
        """
        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[x])):
                pixel = self.pixels[x][y]
                pixel.determine_zero_likelihood(self.instances)
                pixel.determine_one_likelihood(self.instances)

    def determine_likelihood(self, number_count):
        """c
        """
        self.likelihood =\
            float(self.instances) /\
            float(number_count)


class Decision(object):
    """c
    """
    def __init__(self, vals_dict):
        """c
        """
        self.decision = self.decide(vals_dict)

    def decide(self, vals_dict):
        """c
        """
        decision = {
            "value": None,
            "P": None
        }
        for key in vals_dict:
            probability = vals_dict[key]
            if probability >= decision["P"]:
                decision["P"] = probability
                decision["value"] = key
        return decision

class Evaluation(object):
    """c
    """
    def __init__(self):
        """c
        """
        self.MAP_correct = []
        self.MAP_incorrect = []
        self.ML_correct = []
        self.ML_incorrect = []

    def get_MAP_success_rate(self):
        """c
        """
        MAPc = len(self.MAP_correct)
        MAPi = len(self.MAP_incorrect)
        total = MAPc + MAPi
        return (MAPc, MAPi, 100.0 * (float(MAPc) / float(total)))

    def get_ML_success_rate(self):
        """c
        """
        MLc = len(self.ML_correct)
        MLi = len(self.ML_incorrect)
        total = MLc + MLi
        return (MLc, MLi, 100.0 * (float(MLc) / float(total)))

class Classification(object):
    """c
    """
    def __init__(self, MAP_vals, ML_vals):
        """c
        """
        self.MAP = Decision(MAP_vals)
        self.ML = Decision(ML_vals)

class Odds(object):
    """c
    """
    def __init__(self, digit_1, digit_2):
        """c
        """
        self.digit_1 = digit_1
        self.digit_2 = digit_2
        array = []
        for i in range(BLOCK_SIZE):
            array.append([])
            for _ in range(BLOCK_SIZE):
                array[i].append(None)
        self.pixels = array


class Agent(object):
    """c
    """
    def __init__(self):
        """c
        """
        self.digits = {
            0: Digit(0),
            1: Digit(1),
            2: Digit(2),
            3: Digit(2),
            4: Digit(4),
            5: Digit(5),
            6: Digit(6),
            7: Digit(7),
            8: Digit(8),
            9: Digit(9)
        }
        self.confusion_matrix = None
        self.most_confusing = None
        self.odds_list = None
        self.train()

    def whole_shebang(self):
        """c
        """
        self.generate_confusion_matrix()
        print "The Confusion Matrix:=========================="
        self.print_confusion_matrix()
        print "=============================================\n"
        self.generate_most_confusing_odds()
        print "Odds Ratios:==================================="
        self.print_odds()
        print "=============================================\n"

    def print_odds(self):
        """c
        """
        msg = ''
        write_string = None
        write_strings = ['0','1','2','3','4','5','6','7','8','9',\
                         '(','*','&','^','%','$','#','@','!']
        odds_list = self.odds_list
        for odd in odds_list:
            odd_pixels = odd.pixels
            d1_pixels = self.digits[odd.digit_1].pixels
            d2_pixels = self.digits[odd.digit_2].pixels
            pixels_list = [d1_pixels, d2_pixels, odd_pixels]
            msg += "\n#################################\n%d and %d" %\
                (odd.digit_1, odd.digit_2)
            for elem in range(len(pixels_list)):
                msg += '\n\n'
                for row in range(len(pixels_list[elem])):
                    for pixel in range(len(pixels_list[elem][row])):
                        aPixel = pixels_list[elem][row][pixel]
                        const = 10
                        try:
                            num = int(aPixel)
                        except TypeError:
                            num = int(aPixel.one_likelihood * const)
                        if num < -9:
                            num = -9
                        if num > 9:
                            num = 9
                        write_string = write_strings[num]
                        msg += write_string
                    msg += '\n'
        print msg


    def generate_most_confusing_odds(self):
        """c
        """
        odds_list = []
        confusing = self.most_confusing
        con_combos = combinations(confusing, 2)
        for combo in con_combos:
            d1, d2 = combo
            digit_1 = self.digits[d1]
            digit_2 = self.digits[d2]
            odds_obj = Odds(d1, d2)
            pixels = digit_1.pixels
            for i in range(len(pixels)): # Row
                for j in range(len(pixels[i])): # Col
                    coords = (i, j)
                    odds_obj.pixels[i][j] =\
                        self.odds(coords, 1, digit_1, digit_2)
            odds_list.append(odds_obj)
        self.odds_list = odds_list
        return odds_list


    def odds(self, coords, value, digit_1, digit_2):
        """c
        """
        i,j = coords
        likelihood_1 = None
        likelihood_2 = None
        if value == 1:
            likelihood_1 = digit_1.pixels[i][j].one_likelihood
            likelihood_2 = digit_2.pixels[i][j].one_likelihood
        else:
            likelihood_1 = digit_1.pixels[i][j].zero_likelihood
            likelihood_2 = digit_2.pixels[i][j].zero_likelihood
        return likelihood_1 / likelihood_2

    def train(self):
        """c
        """
        training_images, training_labels = training_data()
        for i in range(len(training_labels)):
            image = training_images[i]
            label = training_labels[i]
            digit = self.digits[label]
            digit.instances += 1
            zero_pixels, one_pixels = get_pixel_coords(image)
            for pixel_coord in zero_pixels:
                digit.add_zero(pixel_coord)
            for pixel_coord in one_pixels:
                digit.add_one(pixel_coord)
        for key in self.digits:
            digit = self.digits[key]
            digit.determine_pixel_likelihoods()
            digit.determine_likelihood(len(training_labels))

    def print_confusion_matrix(self):
        print "Class, Correct MAP, Incorrect MAP, MAP Ratio, Correct ML, Incorrect ML, ML Ratio"
        print "================================================================================"
        for key in self.confusion_matrix:
            evaluation = self.confusion_matrix[key]
            MAPc, MAPi, MAPr = evaluation.get_MAP_success_rate()
            MLc, MLi, MLr = evaluation.get_ML_success_rate()
            print "%s\t%d\t%d\t%.2f%%\t%d\t%d\t%.2f%%" %\
                (str(key), MAPc, MAPi, MAPr, MLc, MLi, MLr)


    def generate_confusion_matrix(self):
        """c
        """
        image_data, image_labels = self.digitize()
        evaluations = self.evaluate_classifications(
            image_data,
            image_labels
        )
        self.confusion_matrix = evaluations
        self.generate_most_confusing(4)
        return evaluations


    def generate_most_confusing(self, num):
        matrix = self.confusion_matrix

        most_confusing = []
        while len(most_confusing) < num:
            most_confusing_digit = None
            most_confusing_ratio = 100.0
            for key in matrix:
                if key in most_confusing:
                    continue
                evaluation = matrix[key]
                _, _, MAPr = evaluation.get_MAP_success_rate()
                if MAPr < most_confusing_ratio:
                    most_confusing_ratio = MAPr
                    most_confusing_digit = key
            most_confusing.append(most_confusing_digit)
        self.most_confusing = most_confusing

    def evaluate_classifications(self, image_data, image_labels):
        """c
        """
        evaluations = {
            0: Evaluation(),
            1: Evaluation(),
            2: Evaluation(),
            3: Evaluation(),
            4: Evaluation(),
            5: Evaluation(),
            6: Evaluation(),
            7: Evaluation(),
            8: Evaluation(),
            9: Evaluation()
        }
        for i in range(len(image_labels)):
            label = image_labels[i]
            evaluation = evaluations[label]
            classification = image_data[i]
            MAP_digit = classification.MAP.decision["value"]
            ML_digit = classification.ML.decision["value"]
            if MAP_digit == label:
                evaluation.MAP_correct.append(i)
            else:
                evaluation.MAP_incorrect.append(i)

            if ML_digit == label:
                evaluation.ML_correct.append(i)
            else:
                evaluation.ML_incorrect.append(i)
        return evaluations


    def digitize(self):
        """c
        """
        test_images, test_labels = test_data()
        for i in range(len(test_labels)):
            image = test_images[i]
            classification = self.classify(image)
            # Replace image with extracted data
            test_images[i] = classification
        return test_images, test_labels



    def classify(self, image):
        """c
        """
        MAP_values = {}
        ML_values = {}
        digits = self.digits
        for key in digits:
            digit = digits[key]
            P_class = math.log(digit.likelihood)
            ML_sum = 0
            for x in range(len(image)): # Rows
                for y in range(len(image[x])): # Cols
                    img_pixel = image[x][y]
                    digit_pixel = digit.pixels[x][y]
                    if img_pixel == 1:
                        ML_sum += math.log(digit_pixel.one_likelihood)
                    else:
                        ML_sum += math.log(digit_pixel.zero_likelihood)
            MAP_values[key] = P_class + ML_sum
            ML_values[key] = ML_sum
        return Classification(MAP_values, ML_values)



def get_pixel_coords(image):
    """c
    """
    one_pixels = []
    zero_pixels = []
    for x in range(len(image)):
        for y in range(len(image[x])):
            bit = image[x][y]
            coord = (x, y)
            if bit == 1:
                one_pixels.append(coord)
            else:
                zero_pixels.append(coord)
    return zero_pixels, one_pixels


def get_images(filename):
    """c
    """
    digit_array = []

    path = os.path.join(DIGITS_DIR, filename)
    f = open(path, 'r')
    tmp_array = f.read().splitlines()
    f.close()
    # Read in chunks
    for chunk in range(0, len(tmp_array), BLOCK_SIZE):
        digit_array.append(tmp_array[chunk:chunk + BLOCK_SIZE])
    # Change pixels from chars to 0 or 1
    for x in range(len(digit_array)):
        # Iterate through digit images
        for y in range(len(digit_array[x])):
            # Iterate through image lines
            digit_array[x][y] = list(digit_array[x][y])
            for z in range(len(digit_array[x][y])):
                # Iterate through image line characters
                num = 1
                image_char = digit_array[x][y][z]
                if image_char == ' ':
                    num = 0
                digit_array[x][y][z] = num
    return digit_array


def get_labels(filename):
    """c
    """
    labels = []

    path = os.path.join(DIGITS_DIR, filename)
    f = open(path, 'r')
    labels = f.read().splitlines()
    f.close()
    for index in range(len(labels)):
        labels[index] = int(labels[index])
    return labels

#=====================================================================
# Utils
#---------------------------------------------------------------------
def get_images_and_labels(image_file, label_file):
    """c
    """
    images = get_images(image_file)
    labels = get_labels(label_file)
    return images, labels

def training_data():
    """c
    """
    return get_images_and_labels("trainingimages", "traininglabels")

def test_data():
    """c
    """
    return get_images_and_labels("testimages", "testlabels")

def print_image(image):
    msg = ''
    for x in range(len(image)):
        for y in range(len(image[x])):
            msg += "%d" %(image[x][y])
        msg += '\n'
    print msg

#=====================================================================


#=====================================================================
# Debugging
#---------------------------------------------------------------------

def count_bad_images(num, image_list):
    """c
    """
    count = 0
    indexes = []
    for i in range(len(image_list)):
        if image_list[i].count('\n') < num:
            count += 1
            indexes.append(i)
    return count, indexes

def valid_image_mapping(image_list, label_list):
    """c
    """
    if len(label_list) != len(image_list):
        return False
    return True

#=====================================================================
