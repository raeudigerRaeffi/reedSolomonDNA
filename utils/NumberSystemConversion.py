

class NumberSystemConversion():

    # Split the data
    def two_byte_conversion(data_string):
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
            # converts numbers from base 256 to base 10 numbers
            two_byte_set.append(letter_1*256 + letter_2*1)

        return two_byte_set

    def decimal_to_base(two_byte_set):
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
        base_list.reverse()
        return base_list

    def decimal_to_base_list(input_list):
        base_list = []

        if((len(input_list) % 2) != 0):
            input_list.append(0)

        for i in range(0, len(input_list), 2):
            # (input_list[i+1] << 8) + input_list[i]
            two_bytes = input_list[i] + (input_list[i+1] * 256)
            conv_number = []

            for x in range(0, 3):
                if(two_bytes > 0):
                    conv_number.append(int(two_bytes % 47))
                    two_bytes = int(two_bytes / 47)
                else:
                    break

            if((len(conv_number) > 0) and (conv_number[0] == 0)):
                conv_number[0] = 46
                for x in range(0, (3 - len(conv_number))):
                    base_list.append(46)
            else:
                for x in range(0, (3 - len(conv_number))):
                    base_list.append(0)

            base_list.extend(conv_number)

        return base_list

    def base_list_to_decimal(input_list):
        output = []

        if((len(input_list) % 3) != 0):
            return output  # TODO error behavior

        for i in range(0, len(input_list), 3):
            numbers = []

            # check if the first one is a 0
            if(input_list[i] == 0):
                # remove 0es
                found_number = False
                for x in range(0, 3):
                    if(found_number):
                        numbers.append(input_list[i+x])
                    else:
                        if(input_list[i+x] != 0):
                            numbers.append(input_list[i+x])
                            found_number = True
            elif(input_list[i] == 46):
                # add first 0
                numbers.append(0)
                # remove 46es
                found_number = False
                for x in range(0, 3):
                    if(found_number):
                        numbers.append(input_list[i+x])
                    else:
                        if(input_list[i+x] != 46):
                            numbers.append(input_list[i+x])
                            found_number = True
            else:
                numbers.append(input_list[i])
                numbers.append(input_list[i+1])
                numbers.append(input_list[i+2])

            number = 0
            if(len(numbers) == 3):
                number = numbers[2] * 47
                number = (number + numbers[1]) * 47
                number += numbers[0]
            elif(len(numbers) == 2):
                number = numbers[1] * 47
                number += numbers[0]
            elif(len(numbers) == 1):
                number = numbers[0]

            output.append(number & 0x00FF)
            output.append(number >> 8)

        return output

    # TODO implement the c code here!
    def tobase(nu, base, size):
        nn = []
        for x in range(size):
            nn.append(0)
        if(nu == 0):
            return nu

        div = nu
        i = 0
        while(div != 0):
            nn[i] = int(div % base)
            div = int(div / base)
            i += 1

        return nn

    def frombase(nn, base):
        nu = 0
        basepow = 1
        for n in nn:
            nu += (n * basepow)
            basepow = base

        return nu

    # data_char: string
    # data_b47: list (vector) <- ergebnis wird darein geschrieben, das benötigen wir nicht, wir geben die liste zurück
    def char2pfe(data_char):
        if((len(data_char) % 2) != 0):
            data_char.append(10)  # append \n
