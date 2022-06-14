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
import math

# https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing.pool


# copied from "https://stackoverflow.com/questions/68423946/python-making-and-int-from-8-boolean-byte-values-and-vice-versa"
def bools_to_int(bits):  # WORKS!
    value = 0
    for i, bit in enumerate(bits):
        value |= bit << (len(bits) - i - 1)
    return value


def int_to_bools(value):  # WORKS!
    bits = [False, False, False, False, False, False, False, False]
    for i in range(8):
        if(value != 0):
            bits[7 - i] = ((value % 2) >= 1)
            value = value / 2
        else:
            break

    return bits

# numpy_boolean_array: “NUMPY {'descr': '|b1', 'fortran_order': False, 'shape': (12690688,), }"


def encode(string_file_name, numpy_boolean_array):
    list_of_dna_strings = []
    dna_wheel_instance = dna_wheel()

    # reed codes
    '''
    irr_poly_47 = [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
    inner_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=39,
                                                         payload_length=33,
                                                         symbol_size=30,
                                                         p_factor=7,
                                                         irr_poly=irr_poly_47)
    outer_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=713,
                                                         payload_length=594,
                                                         symbol_size=30,
                                                         p_factor=7,
                                                         irr_poly=irr_poly_47)
    reedWorker = parallelReed(inner_encoder, outer_encoder)
    '''

    # change numpy_boolean_array to an char array
    '''
    length = int(numpy_boolean_array.shape[0] / 8)  # WORKS!
    if((numpy_boolean_array.shape[0] % 8) != 0):
        length += 1
    arr_out = np.empty([length, 1], dtype=int)
    '''
    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in numpy_boolean_array:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            #arr_out[arr_out_pointer, 0] = bools_to_int(byte)
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        #arr_out[arr_out_pointer, 0] = bools_to_int(byte)
        arr_out.append(bools_to_int(byte))

    # convert von 256**2 zu 47**3 #TODO find here a working function
    #two_byte_set = nsc.two_byte_conversion(arr_out)
    #base_list = nsc.decimal_to_base(two_byte_set)
    if((len(arr_out) % 2) != 0):
        arr_out.append(0)
    base_list = nsc.decimal_to_base(arr_out)

    print(base_list[:10])

    # verarbeite daten (array -> string -> liste(matrix)) (594x30)
    dataList = dataToBlock(119, 3, 712, 32, base_list)
    print(dataList)

    # encode daten
    # TODO inner or outer needs to be changeds
    # reedWorker.startRsCode(dataList, 0)

    # verarbeite daten (liste(matrix) -> string) und wandle in basenpaare um
    for block in dataList:
        for x in range(0, 713):
            row = []
            for y in range(0, 39):
                row.append(
                    dna_wheel_instance.number_to_pair[block[x][y]])
            list_of_dna_strings.append(row)

    print(block)

    # output 713*n columns which are 117 nt long

    return list_of_dna_strings


def decode(string_file_name, list_of_dna_strings):
    numpy_boolean_array = []
    dna_wheel_instance = dna_wheel()

    # reed codes
    irr_poly_47 = [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
    inner_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=39,
                                                         payload_length=33,
                                                         symbol_size=30,
                                                         p_factor=7,
                                                         irr_poly=irr_poly_47)
    outer_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=713,
                                                         payload_length=594,
                                                         symbol_size=30,
                                                         p_factor=7,
                                                         irr_poly=irr_poly_47)
    reedWorker = parallelReed(inner_encoder, outer_encoder)

    # wandle daten um (basenpaare -> integer)
    # Base to dezimal
    dataList = []
    block = 0
    for i, row in enumerate(list_of_dna_strings):
        if(i % 713 == 0):
            dataList.append(np.zeros((713, 39)))
            if(i != 0):
                i += 1
        pair = ''
        index = 0
        pos = 0
        for base in row:
            pair += base
            index += 1
            if(index > 2):
                (dataList[i])[i %
                              713][pos] = dna_wheel_instance.pair_to_number[pair]
                index = 0
                pos += 1

    # decode daten
    reedWorker.startRsCode(dataList, 1)

    # verarbeite daten (array -> string)
    finished = False
    for block in dataList:
        for x in range(119, 713):
            for y in range(3, 33):
                output.append(block[x][y])

    # convert von 47**3 zu 256**2
    # TODO find a working implementation

    # change char array to an numpy_boolean_array
    numpy_boolean_array = np.empty([len(output), 1], dtype=bool)  # WORKS!
    arr_out_pointer = 0
    for number in output:
        if(number == 0):
            break
        for bool_val in int_to_bools(number):
            numpy_boolean_array[arr_out_pointer] = bool_val
            arr_out_pointer += 1

    return numpy_boolean_array[0:arr_out_pointer][0]  # WORKS!


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

    # load numpy arrays from files.
    # has boolean values <- convert boolean to numbers and later numbers to boolean. Way more work?
    # use numpy save to save the result

    # https://www.uni-marburg.de/en/fb12/research-groups/distsys/software/mesa

    arr = encode("", np.load("data/Ulysses.npy"))

    print(arr)
    #mask = np.array([2**i for i in range(8)])
    #cov = np.sum(mask * arr.reshape((-1, 8)), axis=1).reshape(arr.shape[0], -1)
    # print(cov)

    # sys.exit("STOP!")

    '''
    temp = gui()
    codingType, filepath = temp.getUserInput(3)

    if(codingType == 0):  # encoding
        # lese daten
        data_string = load_dataset(filepath)
        print(data_string)

        encode()
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
    '''
    '''
    dna_wheel_instance = dna_wheel()

    temp = gui()
    codingType, filepath = temp.getUserInput(3)
    '''
    '''
    inner_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=39,
                                                         payload_length=33,
                                                         symbol_size=1,
                                                         p_factor=7)
    '''
    '''
    irr_poly_47 = [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
    outer_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=713,
                                                         payload_length=594,
                                                         symbol_size=30,
                                                         p_factor=7,
                                                         irr_poly=irr_poly_47)
    inner_encoder = outer_encoder

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
        '''
