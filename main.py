# Import



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
    
    # 1. Load the data
    data_string = load_dataset()
    # 2. Split the data into sets of two bytes
    two_byte_set = two_byte_split(data_string)
    # 3. Transformation to a Galois Field of size 47 (256^2 --> 47^3)
    '''
    Es gibt ein galois Package. Das kann ein GF(47^3) erzeugen.
    Darf ich das nutzen?
    '''
    
    print(two_byte_set)