# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:43:30 2022

@author: Josua Becker
"""
import sys
import utils.gui as gui
import utils.NumberSystemConversion as nsc
import utils.dna_wheel as dna_wheel
import numpy as np

# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool


def load_dataset(filepath='data/the_federal_charter_of_1291.txt'):
    '''
    Load the dataset as string
    Parameters
    ----------
    filepath : string
    Returns
    -------
    data_string : string
    '''
    with open(filepath) as file:
        data_string = file.read()
    return data_string


if __name__ == "__main__":
    temp = gui.gui()
    codingType, filepath = temp.getUserInput(3)

    dna_wheel_instance = dna_wheel()

    if(codingType == 0):  # encoding
        # lese daten
        data_string = load_dataset(filepath)
        print(data_string)

        # convert von 256**2 zu 47**3
        two_byte_set = nsc.two_byte_conversion(data_string)
        base_list = nsc.decimal_to_base(two_byte_set)
        print(base_list)

        # verarbeite daten (array -> string -> liste(matrix)) (594x30)

        block = 0
        column = 0  # v
        row = 0  # >
        list1 = []
        nextBlock = np.array([], [])
        for x in base_list:
            for z in x:
                print("Waiting for content")

        # encode daten
        # TODO outer code
        # TODO index einfügen
        # TODO inner code

        # verarbeite daten (liste(matrix) -> string)

        # wandle daten um (integer -> basenpaare)

        # speicher daten
    elif(codingType == 1):  # decoding
        print("work in progress!")
        # lese daten
        data_string = load_dataset(filepath)

        # wandle daten um (basenpaare -> integer)

        # verarbeite daten (string -> liste(matrix))

        # decode daten
        # TODO inner code
        # TODO schnipsel sortieren, und index entfernen
        # TODO outer code

        # convert von 47**3 zu 256**2

        # verarbeite daten (array -> string)

        # speichere daten

    else:
        sys.exit("It needs to be 0 - Encoding or 1 - Decoding!")
