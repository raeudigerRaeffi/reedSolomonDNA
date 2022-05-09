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
import reedSolomon
import utils.parallelReed as parallelReed

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


def dataToBlock(xStart, yStart, xEnd, yEnd, inputData):
    dataList = []

    print(len(inputData))

    data = np.zeros((713, 39))  # first is column, second is row

    x = (xStart - 1)
    y = yStart
    for d in inputData:
        if(x < xEnd):
            x += 1
        elif(y < yEnd):
            x = 119
            y += 1
        else:
            x = xStart
            y = yStart
            dataList.append(data)
            print(len(dataList))
            data = np.zeros((713, 39))

        # print(x,y)
        data[x][y] = d

    if(len(dataList) == 0):
        dataList.append(data)

    print(len(dataList))
    print(dataList)

    return dataList


if __name__ == "__main__":
    output = []

    dna_wheel_instance = dna_wheel()

    temp = gui.gui()
    codingType, filepath = temp.getUserInput(3)

    inner_encoder = reedSolomon.Generalized_Reed_Solomon(2, 12, 5, 4, 3)
    outer_encoder = reedSolomon.Generalized_Reed_Solomon(2, 12, 5, 4, 3)

    reedWorker = parallelReed(inner_encoder, outer_encoder)

    if(codingType == 0):  # encoding
        # lese daten
        data_string = load_dataset(filepath)
        print(data_string)

        # convert von 256**2 zu 47**3
        two_byte_set = nsc.two_byte_conversion(data_string)
        base_list = nsc.decimal_to_base(two_byte_set)
        print(base_list)

        # verarbeite daten (array -> string -> liste(matrix)) (594x30)
        # TODO check if that is correct, could be that the date is set to 30-long strings and put then together, talk to the others?
        dataList = dataToBlock(119, 3, 712, 32, base_list)

        # encode daten
        reedWorker.startRsCode(dataList, codingType)

        # verarbeite daten (liste(matrix) -> string) und wandle in basenpaare um
        for block in dataList:
            for x in range(119, 713):
                for y in range(3, 33):
                    output.append(
                        dna_wheel_instance.number_to_pair[block[x][y]])

        # speicher daten
        # our data is in output
    elif(codingType == 1):  # decoding
        print("work in progress!")
        # lese daten
        data_string = load_dataset(filepath)

        # wandle daten um (basenpaare -> integer)
        # Base to dezimal
        base_list = []
        pair = ''
        index = 0
        for base in data_string:
            pair += base
            index += 1
            if(index > 2):
                base_list.append(dna_wheel_instance.pair_to_number[pair])
                index = 0

        # verarbeite daten (string -> liste(matrix))
        # TODO check if that is correct, could be that the date is set to 30-long strings and put then together, talk to the others?
        dataList = dataToBlock(0, 0, 712, 38, base_list)

        # decode daten
        reedWorker.startRsCode(dataList, codingType)

        # convert von 47**3 zu 256**2
        # TODO

        # verarbeite daten (array -> string)
        for block in dataList:
            for x in range(119, 713):
                for y in range(3, 33):
                    output[index] = block[x][y]
                    index += 1

        # speichere daten
        # our data is in output
        # TODO
    else:
        sys.exit("It needs to be 0 - Encoding or 1 - Decoding!")
