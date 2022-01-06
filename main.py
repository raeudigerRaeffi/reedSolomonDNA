# Import
import numpy as np
import galois
import time
import random


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
    
    
    # index oder poly oder andere???
    array = list(range(47))
    array.append('*')
    random.shuffle(array)
    
    # Dict für integer - DNA codon? --> Klasse
    dna_codon_wheel = {
        'ATC':None, 'ATA':None, 'ATG':None,  # 'ATT':None,
        'ACT':None, 'ACA':None, 'ACG':None,  # 'ACC':None,
        'AAT':None, 'AAC':None, 'AAG':None,  # 'AAA':None,
        'AGT':None, 'AGC':None, 'AGA':None,  # 'AGG':None,  
        
        'GTC':None, 'GTA':None, 'GTG':None, # 'GTT':None,
        'GCT':None, 'GCA':None, 'GCG':None, # 'GCC':None,
        'GAT':None, 'GAC':None, 'GAG':None, # 'GAA':None,
        'GGT':None, 'GGC':None, 'GGA':None, # 'GGG':None, 
        
        'TTC':None, 'TTA':None, 'TTG':None, # 'TTT':None,
        'TCT':None, 'TCA':None, 'TCG':None, # 'TCC':None, 
        'TAT':None, 'TAC':None, 'TAG':None, # 'TAA':None,
        'TGT':None, 'TGC':None, 'TGA':None, # 'TGG':None,
        
        'CTC':None, 'CTA':None, 'CTG':None, # 'CTT':None,
        'CCT':None, 'CCA':None, 'CCG':None, # 'CCC':None,
        'CAT':None, 'CAC':None, 'CAG':None, # 'CAA':None,
        'CGT':None, 'CGC':None, 'CGA':None  # 'CGG':None, 
    }
    
    index = 0
    for key in dna_codon_wheel:
        dna_codon_wheel[key] = array[index]
        index += 1
    print(dna_codon_wheel['37'])
    
    
    
    
    
    
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