# Import
import numpy as np
import time
import random
import utils.NumberSystemConversion as nsc
import utils.dna_wheel as dna_wheel


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


if __name__ == '__main__':
    '''
    Main function
    '''

    dna_wheel_instance = dna_wheel()
    data_string = load_dataset()

    two_byte_set = nsc.two_byte_conversion(data_string)
    base_list = nsc.dezimal_to_base(two_byte_set)
    print(base_list)

    # Performance counter
    print(str(time.perf_counter()/1000)+' s')
