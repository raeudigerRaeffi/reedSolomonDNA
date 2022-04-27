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

    inner_encoder = reedSolomon.Generalized_Reed_Solomon(2,12,9,4,3) #n 12 k 5 c 2 r 7 d 1 -> 5 + 9 - (3 -1)
    # 3- 2 = 1   12 -3- 2 = 7 3-1 = 2
    msg = inner_encoder.encode([ 5, 6, 4, 10,3,5,5,2,5])
    msg_org = np.copy(msg)
    msg[1] = 0
    print("tainted",msg)
    dec_msg = inner_encoder.decode(msg)
    print("org",msg_org)
    print("dec",dec_msg)
    print([ 5, 6, 4, 10,3,5,5,2,5] == dec_msg)

    #test_normal_rs = reedSolomon.Generalized_Reed_Solomon(5,12,6,4,3)
    #normal_msg = test_normal_rs.encode([ 5, 6, 4, 10,3,5])
    #normal_msg[2] = 11
    #dec_test_normal = test_normal_rs.decode(normal_msg)
    #print("dec",dec_test_normal)
   
   
    #manual_irr_poly = [1, 13, 15, 22, 45, 19, 34, 10, 17, 5, 41, 21, 12, 3, 23, 17, 27, 8, 34, 32, 7, 40, 41, 1, 32, 26, 24, 32, 37, 5, 1]
    #paper_rs = reedSolomon.Generalized_Reed_Solomon(47,713,594,30,1,manual_irr_poly)
    #test_msg = np.random.random_integers(0,46,(30,594))
    #test_msg_transformed = paper_rs.convert_to_symbol_array(test_msg)
    #print(len(test_msg_transformed))
    #paper_rs.encode(test_msg_transformed)
    #encode_msg = inner_encoder.systematic_encoding(msg)
    
    #print("message bit to be replaces", encode_msg[7])
    #encode_msg[9] = 0
    #encode_msg[7] = 9
    #print(encode_msg)
     
    #inner_encoder.systematic_decode(encode_msg)
    #print(inner_encoder.decode(encode_msg) == msg)
    #print(base_list)

    # Performance counter
    print(str(time.perf_counter()/1000)+' s')


    # n = k +r  k = information r = parity bits
    # n / p -> k /p und r/p
    # p = 23 713 
    # k % p != 0 r %p = 0
    # wähle p so dass r /p   n = 713,k = 594,r=119 und p = 17

    #veränderung von p führt zu fehler -> 
    ##veränderung von field size führt zu fehler
