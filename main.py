# Import
import numpy as np
import time
import random
import utils.NumberSystemConversion as nsc
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




if __name__ == '__main__':
    '''
    Main function
    '''
    
    dna_wheel_instance = dna_wheel()
    print(dna_wheel_instance.pair_to_number)
    
    
    
    # 1. Load the data
    data_string = load_dataset()
    # 2. Split the data into sets of two bytes
    two_byte_set = nsc.two_byte_conversion(data_string)
    base_list = nsc.dezimal_to_base(two_byte_set)
    print(base_list)
    
    
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
    # 3. Transformation to a Galois Field of size 47 (256^2 --> 47^3)
    #GF47_3 = galois.GF(47**3)
    #print(GF47_3)
    
    # Performance counter
    #print(str(time.perf_counter()/1000)+' s')
