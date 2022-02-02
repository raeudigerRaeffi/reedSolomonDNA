# Import
import numpy as np
import time
import random
import utils.NumberSystemConversion as nsc
import utils.dna_wheel as dna_wheel
import utils
import reedSolomon


if __name__ == '__main__':
    '''
    Main function
    '''
    
    # Initilize needed Class Objects
    dna_wheel_instance = dna_wheel()
    data_string = utils.load_dataset()
    
    ##### TESTAREA
    
    
    ####

#    two_byte_set = nsc.two_byte_conversion(data_string)
#    base_list = nsc.decimal_to_base(two_byte_set)
#    inner_encoder = reedSolomon.Reed_Solomon(11,10,6)
#    #inner_encoder.generator_polynominal = np.polynomial.polynomial.Polynomial([1,8,5,3,1])
#    msg = np.array([3,0,0,0,0,1])
#    encode_msg = inner_encoder.encode(msg)
#    print(encode_msg)
#    print(inner_encoder.decode(encode_msg))
#    print(inner_encoder.decode(encode_msg) == msg)
#    #print(base_list)
#
#    # Performance counter
#    print(str(time.perf_counter()/1000)+' s')
