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

    # Boolean (Array[n:1]) -> 256**2 (List)
    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in numpy_boolean_array:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        arr_out.append(bools_to_int(byte))

    # 256**2 (List) -> 47**3 (List)
    base_list = nsc.char2pfe(arr_out)

    # 47**3 (List) -> 47**3 (Array[Array[713,39]])
    dataList = []
    dataList.append(np.zeros((713, 39), dtype=int))

    block = 0
    x = 119
    y = 2
    for d in base_list:
        if(y < 32):
            y += 1
        elif(x < 712):
            y = 3
            x += 1
        else:
            x = 119
            y = 3
            dataList.append(np.zeros((713, 39), dtype=int))
            block += 1

        (dataList[block])[x][y] = d

    # encode daten
    # TODO inner or outer needs to be changeds
    # reedWorker.startRsCode(dataList, 0)

    # 47**3 (Array[Array[713,39]]) -> ACGT (List(x*713) of Strings(117))
    for block in dataList:
        for x in range(0, 713):
            row = ""
            for y in range(0, 39):
                row += dna_wheel_instance.number_to_pair[block[x][y]]
            list_of_dna_strings.append(row)

    return list_of_dna_strings


def decode(string_file_name, list_of_dna_strings):
    numpy_boolean_array = []
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

    # ACGT (List(x*713) of Strings(117)) -> 47**3 (Array[Array[713,39]])
    dataList = []
    block = 0
    for i, row in enumerate(list_of_dna_strings):
        if(i % 713 == 0):
            dataList.append(np.zeros((713, 39), dtype=int))
            if(i > 0):
                block += 1
        pair = ''
        index = 0
        pos = 0
        for base in row:
            pair += base
            index += 1
            if(index > 2):
                (dataList[block])[i %
                                  713][pos] = dna_wheel_instance.pair_to_number[pair]
                pair = ''
                index = 0
                pos += 1

    # decode daten
    # reedWorker.startRsCode(dataList, 1)

    # 47**3 (Array[Array[713,39]]) -> 47**3 (List) #TODO here could be an error
    output = []
    for block in dataList:
        for x in range(119, 713):
            for y in range(3, 33):
                output.append(block[x][y])

    # 47**3 (List) -> 256**2 (List)
    converted_output = nsc.pfe2char(output)

    # 256**2 (List) -> Boolean (Array[n:1])
    numpy_boolean_array = np.empty(
        [int(len(converted_output)*8), 1], dtype=bool)  # WORKS!
    arr_out_pointer = 0
    for number in converted_output:
        for bool_val in int_to_bools(number):
            numpy_boolean_array[arr_out_pointer] = bool_val
            arr_out_pointer += 1

    return numpy_boolean_array[0:arr_out_pointer]  # WORKS!


if __name__ == "__main__":
    # load numpy arrays from files.
    # has boolean values <- convert boolean to numbers and later numbers to boolean. Way more work?
    # use numpy save to save the result

    # https://www.uni-marburg.de/en/fb12/research-groups/distsys/software/mesa

    # Teste data -> encode() -> decode() -> data (ohne rs codes)
    print("Load File...")
    # input_arr = np.load("data/La_Jeunesse.npy") # kurzes test-set
    input_arr = np.load("data/Ulysses.npy")  # langes test-set

    print("Encoding...")
    arr = encode("", input_arr)
    print("Decoding...")
    arr2 = decode("", arr)

    errors = 0
    for i, bool_val in enumerate(input_arr):
        if(i < len(arr2)):
            if(arr2[i] != bool_val):
                errors += 1

    print(errors)

    '''
    temp = gui()
    codingType, filepath = temp.getUserInput(3)

    if(codingType == 0):  # encoding
        print("encode")
    elif(codingType == 1):  # decoding
        print("decode")
    else:
        sys.exit("It needs to be 0 - Encoding or 1 - Decoding!")
    '''
    '''
    # Teste data -> block -> liste Basenpaare -> block -> data
    dna_wheel_instance = dna_wheel()

    # lade daten
    input_arr = np.load("data/La_Jeunesse.npy")

    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in input_arr:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        arr_out.append(bools_to_int(byte))

    # convert von 256**2 zu 47**3
    base_list = nsc.char2pfe(arr_out)

    # 47**3 (List) -> 47**3 (Array[Array[713,39]])
    # dataList = dataToBlock(119, 3, 712, 32, base_list)
    dataList = []
    dataList.append(np.zeros((713, 39), dtype=int))

    block = 0
    x = 119
    y = 2
    for d in base_list:
        if(y < 32):
            y += 1
        elif(x < 712):
            y = 3
            x += 1
        else:
            x = 119
            y = 3
            dataList.append(np.zeros((713, 39), dtype=int))
            block += 1

        (dataList[block])[x][y] = d

    # 47**3 (Array[Array[713,39]]) -> ACGT (List(x*713) of Strings(117))
    list_of_dna_strings = []
    for block in dataList:
        for x in range(0, 713):
            row = ""
            for y in range(0, 39):
                row += dna_wheel_instance.number_to_pair[block[x][y]]
            if(len(row) != 117):
                print(len(row))
            list_of_dna_strings.append(row)

    # ACGT (List(x*713) of Strings(117)) -> 47**3 (Array[Array[713,39]])
    dataList = []
    block = 0
    for i, row in enumerate(list_of_dna_strings):
        if(i % 713 == 0):
            dataList.append(np.zeros((713, 39), dtype=int))
            if(i > 0):
                block += 1
        pair = ''
        index = 0
        pos = 0
        for base in row:
            pair += base
            index += 1
            if(index > 2):
                (dataList[block])[i %
                                  713][pos] = dna_wheel_instance.pair_to_number[pair]
                pair = ''
                index = 0
                pos += 1

    errors = 0
    for b, block in enumerate(dataList):
        for x, list1 in enumerate(block):
            for y, ele in enumerate(list1):
                if(ele != (dataList[b])[x][y]):
                    errors += 1

    print(errors)

    # Teste 256^2 -> 47^3 -> 256^3 converting
    input_arr = np.load("data/La_Jeunesse.npy")

    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in input_arr:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        arr_out.append(bools_to_int(byte))

    # convert von 256**2 zu 47**3
    base_list = nsc.char2pfe(arr_out)

    # convert von 47**3 zu 256**2
    reverted_test_set = nsc.pfe2char(base_list)

    # print(reverted_test_set)

    errors = 0
    for i, test in enumerate(arr_out):
        if(test != reverted_test_set[i]):
            print(test, "=>", reverted_test_set[i])
            errors += 1

    print(errors)

    # Teste Boolean -> Int -> Boolean converting
    input_arr = np.load("data/La_Jeunesse.npy")

    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in input_arr:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        arr_out.append(bools_to_int(byte))

    numpy_boolean_array = np.empty(
        [int(len(reverted_test_set)*8), 1], dtype=bool)  # WORKS!
    arr_out_pointer = 0
    for number in reverted_test_set:
        for bool_val in int_to_bools(number):
            numpy_boolean_array[arr_out_pointer] = bool_val
            arr_out_pointer += 1

    errors = 0
    for i, test in enumerate(input_arr):
        if(test != numpy_boolean_array[i]):
            print(test, "=>", numpy_boolean_array[i])
            errors += 1

    print(errors)
    
    # Teste Boolean -> 256^2 -> 47^3 -> 256^2 -> Boolean converting
    input_arr = np.load("data/La_Jeunesse.npy")

    arr_out = []
    byte = [False, False, False, False, False, False, False, False]
    byte_pointer = 0
    arr_out_pointer = 0
    for bit in input_arr:
        byte[byte_pointer] = bit
        if(byte_pointer == 7):
            arr_out.append(bools_to_int(byte))
            arr_out_pointer += 1
            byte_pointer = 0
        else:
            byte_pointer += 1

    if(byte_pointer != 0):  # WORKS!
        while(byte_pointer < 8):
            byte[byte_pointer] = False
            byte_pointer += 1
        arr_out.append(bools_to_int(byte))

    # convert von 256**2 zu 47**3
    base_list = nsc.char2pfe(arr_out)

    # convert von 47**3 zu 256**2
    reverted_test_set = nsc.pfe2char(base_list)

    numpy_boolean_array = np.empty(
        [int(len(reverted_test_set)*8), 1], dtype=bool)  # WORKS!
    arr_out_pointer = 0
    for number in reverted_test_set:
        for bool_val in int_to_bools(number):
            numpy_boolean_array[arr_out_pointer] = bool_val
            arr_out_pointer += 1

    errors = 0
    for i, test in enumerate(input_arr):
        if(test != numpy_boolean_array[i]):
            print(test, "=>", numpy_boolean_array[i])
            errors += 1

    print(errors)
    '''
