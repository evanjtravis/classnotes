#!/usr/bin/env python
#TODO in readme, run this in local dir, relative paths

import os
DIGITS_DIR = "digitdata/"
BLOCK_SIZE = 28

class Pixel(object):
    """c
    """
    def __init__(self):
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

class Class(object):
    """c
    """
    def __init__(self, digit):
        """c
        """
        self.digit = digit
        digit_pixels = []
        for i in range(BLOCK_SIZE):
            digit_pixels.append([])
            for _ in range(BLOCK_SIZE):
                digit_pixels[i].append(Pixel())
        self.digit_pixels = digit_pixels
        self.instances = 0
        self.likelihood = 0

    def add_zero(self, coords):
        """c
        """
        x, y = coords
        self.digit_pixels[x][y].zero_count += 1

    def add_one(self, coords):
        """c
        """
        x, y = coords
        self.digit_pixels[x][y].one_count += 1

    def determine_pixel_likelihoods(self):
        """c
        """
        for x in range(len(self.digit_pixels)):
            for y in range(len(self.digit_pixels[x])):
                pixel = self.digit_pixels[x][y]
                pixel.determine_zero_likelihood(self.instances)
                pixel.determine_one_likelihood(self.instances)

    def determine_likelihood(self, number_count):
        """c
        """
        self.likelihood =\
            float(self.instances) /\
            float(number_count)


class Agent(object):
    """c
    """
    def __init__(self):
        """c
        """
        self.digits = {
            0: Class(0),
            1: Class(1),
            2: Class(2),
            3: Class(2),
            4: Class(4),
            5: Class(5),
            6: Class(6),
            7: Class(7),
            8: Class(8),
            9: Class(9)
        }
        self.train()

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

    def digitize(self):
        """c
        """
        test_images, test_labels = test_data()
        for i in range(len(test_labels)):
            image = test_images[i]
            label = test_labels[i]
            guess = self.guess_digit(image)

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


def trim_left_cols(image):
    """c
    """
    zeroes_found = True
    while zeroes_found:
        cells = []
        tmp_image = image[:]
        for line in range(len(image)):
            cells.append(image[line][0])
            image[line] = image[line][1:]
        if 1 in cells:
            zeroes_found = False
            image = tmp_image[:]
    return image

def trim_right_cols(image):
    """c
    """
    zeroes_found = True
    while zeroes_found:
        cells = []
        tmp_image = image[:]
        for line in range(len(image)):
            cells.append(image[line][-1])
            image[line] = image[line][:-1]
        if 1 in cells:
            zeroes_found = False
            image = tmp_image[:]
    return image

def trim_top_rows(image):
    """c
    """
    zeroes_found = True
    while zeroes_found:
        cells = image[0]
        if 1 in cells:
            zeroes_found = False
        else:
            image = image[1:]
    return image

def trim_bottom_rows(image):
    """c
    """
    zeroes_found = True
    while zeroes_found:
        cells = image[-1]
        if 1 in cells:
            zeroes_found = False
        else:
            image = image[:-1]
    return image

def trim_digit_array(digit_array):
    """c
    """
    for i in range(len(digit_array)):
        image = digit_array[i]
    # trim left 0 cols
        image = trim_left_cols(image)
    # trim right 0 cols
        image = trim_right_cols(image)
    # trim top 0 rows
        image = trim_top_rows(image)
    # trim bottom 0 rows
        image = trim_bottom_rows(image)
        digit_array[i] = image
    return digit_array


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
    # TODO see if trimming improves algorithm
    # TODO would have to guarantee centered or at least consistent
    # character mapping from one entry to the next...
    #digit_array = trim_digit_array(digit_array)
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
