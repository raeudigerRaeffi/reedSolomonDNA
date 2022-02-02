

class NumberSystemConversion():

    # Split the data
    def two_byte_conversion(data_string:str):
        '''
        The string length is checked. If the number of characters in the string
        is even, a direct division into 2-byte subsets is possible, otherwise a
        space must be inserted at the end of the text.
        The 2-byte subset is converted by a polynomial to a decimal number.
        Return the list of 2-byte subset decimals.
        
        Parameters
        ----------
        data_string : string    
        
        Returns
        -------
        two_byte_set : list of 2-byte subset decimals
        '''
        two_byte_set = []
        if len(data_string) % 2 != 0:
            data_string = data_string + ' '

        for i in range(0, len(data_string), 2):
            letter_1 = ord(data_string[i])
            letter_2 = ord(data_string[i+1]) 
            # hmh.
            two_byte_set.append(letter_1*256 + letter_2*1) #converts numbers from base 256 to base 10 numbers

        return two_byte_set

    def decimal_to_base(two_byte_set:list):
        '''
        
        Parameters
        ----------
        two_byte_set : list    
        
        Returns
        -------
        
        '''
        base_list = []
        for decimal in two_byte_set:
            representation_array = []
            if decimal == 0:
                representation_array.append(0)
                base_list.append(representation_array)
            while decimal:
                representation_array.append(int(decimal % 47))
                decimal //= 47
            base_list.append(representation_array[::-1])
        # ich glaube das ist nicht nötig weil base_list eine triplet darstellung des two_byte_set ist und nicht reversed werden darf
        base_list.reverse()
        return base_list
