import numpy as np


class Reed_Solomon() :

    def __init__(self, field_size:int, message_length:int, payload_length:int) -> None:
        self.field_size = field_size
        self.message_length = message_length
        self.payload_length = payload_length
        self.two_s = message_length - payload_length
        self.generator_polynominal = self.return_generator_polynominal()
        
    # params message : np.array of length payload_length
    # output np.array of length message_length
    def encode(self, message):
        if len(message) != self.payload_length:
            raise "message has not the right length"
            
        message = np.polynomial.polynomial.Polynomial(message)
        parity = ([0] * (self.two_s +1))
        parity[self.two_s] = 1
        parity = np.polynomial.polynomial.Polynomial(parity)
        # message times x**2s
        new_message = np.polymul(parity,message)[0]

        # obtain parity elements to add to message
        # thus message becomes divisible by generator
        r = np.polynomial.polynomial.polydiv(new_message.coef,self.generator_polynominal.coef)[1] % self.field_size
        r = np.array([(a -self.field_size) * -1 if a != 0 else a for a in r ])
        r = np.polynomial.polynomial.Polynomial(r)

        # add polynominals together
        message_out = new_message + r

        # send coefficents out
        return message_out.coef
    
    # params message : np.array of length message_length
    # output np.array of length payload_length
    def decode(self, recieved_message):
        pass

    def return_generator_polynominal(self):
        pass

    
    def find_primitive_element():
        pass
