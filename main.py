# Import
import numpy as np
import galois
import time


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
    Check if the given string is even, if not append a space.
    Split the string into a list of 2 byte subsets of the given string.
    
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
    # BYTE CONVERTIERUNG FEHLT NOCH ---------> [    two_byte_set.encode('utf-8')    ]
    return two_byte_set


if __name__ == '__main__':
    '''
    Main function
    '''
    
    # 1. Load the data
    data_string = load_dataset()
    # 2. Split the data into sets of two bytes
    two_byte_set = two_byte_split(data_string)
    # 3. Transformation to a Galois Field of size 47 (256^2 --> 47^3)
    GF47_3 = galois.GF(47**3)
    print(GF47_3)
    
    
    # Performance counter
    print(str(time.perf_counter()/1000)+' s')
