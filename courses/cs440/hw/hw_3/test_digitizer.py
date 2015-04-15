#!/usr/bin/env python

import digitizer
ERRORS = 0


def test_image_label_pair(image_file, label_file):
    """c
    """
    global ERRORS
    images = digitizer.get_images(image_file)
    labels = digitizer.get_labels(label_file)
    is_valid = digitizer.valid_image_mapping(images, labels)
    if not is_valid:
        print "INVALID %s : %s" %(image_file, label_file)
        ERRORS += 1


def main():
    """c
    """
    global ERRORS
    test_image_label_pair("testimages", "testlabels")
    test_image_label_pair("trainingimages", "traininglabels")
    print "***Testing complete. %d tests failed." %(ERRORS)
    ERRORS = 0


if __name__ == "__main__":
    main()
