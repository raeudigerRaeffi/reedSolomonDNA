# Import
import numpy as np
import time
import random
import utils.dna_wheel as dna_wheel

# Load DataSet (easy load)
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


# Split the data
def two_byte_split(data_string):
    '''
    Split a string to a list with two byte strings
    Parameters
    ----------
    data_string : string    
    Returns
    -------
    two_byte_set : list
    '''
    two_byte_set = []
    if len(data_string)%2 != 0:
        data_string = data_string + ' '                                                      #
    for i in range(0, len(data_string), 2):
        two_byte_set.append(data_string[i] + data_string[i+1])
    return two_byte_set


if __name__ == '__main__':
    '''
    Main function
    '''
    
    dna_wheel_instance = dna_wheel()
    print(dna_wheel_instance.pair_to_number)
    
    
    
    
    # 1. Load the data
    data_string = load_dataset()
    # 2. Split the data into sets of two bytes
    two_byte_set = two_byte_split(data_string)
    
    # Unique byte set
    unique_byte_set = []
    for pair in two_byte_set:
        if pair not in unique_byte_set:
            unique_byte_set.append(pair)

    
    
    
    byte_integer_dict = {}
    
    
    # 3. Transformation to a Galois Field of size 47 (256^2 --> 47^3)
    
   
    #print(GF47.irreducible_poly)
    #print(array)
    #print(array.view(GF47_3))
    #print(GF47_3[0])
    
    
    # Performance counter
    print(str(time.perf_counter()/1000)+' s')