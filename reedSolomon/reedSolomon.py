 
import numpy as np
import galois as gl
from math import gcd 

class Reed_Solomon() :

    # Inner Code
    # shorten code with 0 appended and systematic encoding

    #Outercode
    #Encoding with discrete foruier tranform

    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int) -> None:
        self.field_size = field_size
        self.galois_field = gl.GF(field_size**symbol_size)
        self.message_length = message_length
        self.payload_length = payload_length
        self.two_s = message_length - payload_length
        self.primitive_element = self.find_primitive_element()
        self.generator_polynominal = self.return_generator_polynominal()
        self.gen_roots = self.generator_polynominal.roots()
        
    # params message : np.array of length payload_length
    # output np.array of length message_length
    def systematic_encoding(self, message):
        if len(message) != self.payload_length:
            print(len(message))
            raise  "message has not the right length"
        #n-1 n = länge deiner nachricht nachrichtpolynomon von n-1ten grad 2x^2 +4x +1
        # c =  m * x^2s s = Anzahl der Fehler die zu korregieren sind
        # c %gen
        message = self.create_poly(message)
        
        parity = ([0] * (self.two_s +1))
        parity[self.two_s] = 1
        parity = self.create_poly(parity)
        #print(message)
        print("parity",parity)
        # message times x**2s
        new_message = parity * message
        #print(new_message)
        # obtain parity elements to add to message
        # thus message becomes divisible by generator
        
        r = new_message % self.generator_polynominal
        
        #print("r",r)
        # add polynominals together
        message_out = new_message - r
        #print("msg out",message_out)
        # send coefficents out
        return message_out.coeffs[::-1]
    

    def encoding(self,message):
        #input column zu gf element
        #output n - k entries from start 0 remaining k = input
        # idfgt auf output und return



    # params message : np.array of length message_length
    # output np.array of length payload_length
    def decode(self, recieved_message):
        print("len gen roots",len(self.gen_roots))
        msg = self.create_poly(recieved_message)
        print(msg) 
        # check if message divides by generator if yes no error -> return message indexed at values of k
        if (msg % self.generator_polynominal) ==self.create_poly([0]):
             
            return recieved_message[self.two_s:self.message_length]
        # error detected
        else:
            # steps erasure calculations performen -> dft
            # Steps : calc syndrome -> error polynominal(berlekamp) -> error locations(chien search) -> error magnitude(forney algo) -> error corrector
            # get syndrome 
            syndrome = self.calc_syndrome(msg)
            #syndrome = msg % self.generator_polynominal
            # get error polynominal
            print(syndrome)
            #error_polynominal = gl.berlekamp_massey(syndrome.coeffs[::-1])
            
            error_polynominal = gl.berlekamp_massey(self.galois_field(syndrome[::-1]))

            error_locations = error_polynominal.roots()
            #find inverse of locations

            # get error location
            with self.galois_field.display("power"):
                print("error locations",error_locations)
            

    def calc_syndrome(self,message_ploynominal):
        syndrome = []
        # evaluate message polynominal 2s times with primitive element by raising element to power 0 < i < 2s x**i
        for i in range(1,self.two_s+1):
            print("poer to eval syndrom",i)
            syndrome.append(message_ploynominal(self.primitive_element**i))
        #for i in self.gen_roots: # replace with gen roots
        #    syndrome.append(message_ploynominal(i))
        return syndrome 

    # uses berlekamp massey algorithm due to better execution time
    def calc_error_polynominal(self, syndrome):
        i = 0
        n = len(syndrome)
        error_loc = np.zeros(n)
        error_loc[0] = 1
        L = 0
        error_l = np.zeros(n)
        error_l[0] = 1
        l = -1
        discrepancy_l = 1
        while i < n:
            syndrome_values = syndrome[i-L:i]
            # flips syndrome values due to s_(k-i) * omega_k requirement
            discrepancy_current = (syndrome[i] + np.dot(error_loc[0:L],syndrome_values[::-1])) % self.field_size
            if discrepancy_current != 0:
                temp_copy = np.copy(error_loc)
                p = np.zeros(n)
                for j in range(0, l):
                    if error_l[j] != 0:
                        p[j + i - l] = error_l[j]
                error_loc = (error_loc + p) % self.field_size

                if (2 * L) <= i:
                    l = i
                    error_l = temp_copy
                    discrepancy_l = discrepancy_current
                    L = i + 1 - L
            i = i + 1
        return error_loc

    # uses chien search algorithm
    def calc_error_locations(self, error_polynominal):
        error_locations = []
        polynominal_to_evaluate = np.polynomial.polynomial.Polynomial(error_polynominal)
        # evaluate polynominal for all elements of GF(p) if error polynominal is 0 location is found
        for i in range(0,self.field_size):
            y = polynominal_to_evaluate(i) % self.field_size
            if y == 0:
                error_locations.append(i)
        return error_locations
         

    def return_generator_polynominal(self):
        
        output_poly = self.create_poly([-self.primitive_element**0,1])
        for i in range(1,self.two_s): 
            output_poly *= self.create_poly([-self.primitive_element**i ,1])
         
        return output_poly

    
    def find_primitive_element(self):
    
        return self.galois_field.primitive_elements[0]
         

    def create_poly(self,data):
        return  gl.Poly(data[::-1],self.galois_field)
    
    def find_inverse(self,number):
        return self.galois_field(1) / number
    
    def convert_to_symbol_array(matrix):
        output = []
        for i in range(0,matrix.shape[1]):
            output.append(int(gl.Poly(matrix[:,i],field=self.galois_field)))
        return np.array(output)
         