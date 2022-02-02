def utils_import_test():
    print("Utils imported")
    

def load_dataset(filepath='data/the_federal_charter_of_1291.txt'):
    '''
    Load the given dataset into a string
    
    Parameters
    ----------
    filepath : string
    
    Returns
    -------
    data_string : string
    '''
    try:
        with open(filepath) as file:
            data_string = file.read()
        return data_string
    except Exception as error:
        print('Loading the Dataset failed: '+str(error.args[1]))
        
        
def save_result_to_txt(filepath:str, filename:str, result_string:str):
    '''
    Create a new text file into the decode folder.
    Save the decoded string to text file.
    
    Parameters
    ----------
    filepath : string
    filename: string
    result_string: string
    
    Returns
    -------
    None
    '''
    try:
        file = open(filepath+filename+'.txt', 'x')
        file.write(result_string)
        file.close
    except Exception as error:
        print('Failed while saving: '+str(error.args[1]))