import numpy as np
from math import gcd 

class Reed_Solomon() :

    def __init__(self, field_size:int, message_length:int, payload_length:int) -> None:
        self.field_size = field_size
        self.message_length = message_length
        self.payload_length = payload_length
        self.two_s = message_length - payload_length
        self.primitive_element = self.find_primitive_element()
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
        r = self.poly_division_in_field(new_message,self.generator_polynominal)
        r = np.polynomial.polynomial.Polynomial(np.array([(a -self.field_size) * -1 if a != 0 else a for a in r ]))

        # add polynominals together
        message_out = new_message + r

        # send coefficents out
        return message_out.coef
    
    # params message : np.array of length message_length
    # output np.array of length payload_length
    def decode(self, recieved_message):
        msg = np.polynomial.polynomial.Polynomial(recieved_message)
        # check if message divides by generator if yes no error -> return message indexed at values of k
        if np.array_equal((msg % self.generator_polynominal).coef % self.field_size, np.zeros(self.two_s)):
            return recieved_message[self.two_s:self.message_length]
        # error detected
        else:
            # Steps : calc syndrome -> error polynominal(berlekamp) -> error locations(chien search) -> error magnitude(forney algo) -> error corrector
            # get syndrome
            syndrome = self.calc_syndrome(msg)
            # get error polynominal
            error_polynominal = self.calc_error_polynominal(syndrome)
            print(error_polynominal)
            

    def calc_syndrome(self,message_ploynominal):
        syndrome = []
        # evaluate message polynominal 2s times with primitive element by raising element to power 0 < i < 2s x**i
        for i in range(1,self.two_s+1):
            syndrome.append(message_ploynominal((self.primitive_element**i)%self.field_size) % self.field_size)
        return np.array(syndrome)

    # uses berlekamp massey algorithm due to better execution time
    def calc_error_polynominal(self, syndrome):
       pass
         

    def return_generator_polynominal(self):
        output_poly = np.polynomial.polynomial.Polynomial(np.array([-self.primitive_element,1]))
        for i in range(2,self.two_s +1):
            output_poly *= np.polynomial.polynomial.Polynomial(np.array([-self.primitive_element**i,1]))
        return output_poly

    
    def find_primitive_element(self):
        required_set = {num for num in range(1, self.field_size) if gcd(num, self.field_size) }
        # wäre mehr effizient hier nicht alle elemente zu suchen 
        all_primitives = [g for g in range(1, self.field_size) if required_set == {pow(g, powers, self.field_size) for powers in range(1, self.field_size)}]
        if len(all_primitives) == 0:
            raise "No primitive elements found"
        return all_primitives[0]
    
    def poly_division_in_field(self,poly1,poly2):
        return np.polynomial.polynomial.polydiv(poly1.coef,poly2.coef)[1] % self.field_size
         