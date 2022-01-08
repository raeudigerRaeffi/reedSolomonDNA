# Import
import numpy as np
import time
import random
import utils.NumberSystemConversion as nsc
import utils.dna_wheel as dna_wheel
import reedSolomon

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
    base_list = nsc.decimal_to_base(two_byte_set)
    inner_encoder = reedSolomon.Reed_Solomon(11,10,6)
    #inner_encoder.generator_polynominal = np.polynomial.polynomial.Polynomial([1,8,5,3,1])
    print(inner_encoder.encode(np.array([3,0,0,0,0,1])))
    print(inner_encoder.find_primitive_element())
    #print(base_list)

    # Performance counter
    print(str(time.perf_counter()/1000)+' s')
