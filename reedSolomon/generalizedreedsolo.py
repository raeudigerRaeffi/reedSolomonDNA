from dataclasses import field
import numpy as np
import galois as gl
from .basereedsolomon import Base_Reed_Solomon




class Generalized_Reed_Solomon(Base_Reed_Solomon):
    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int,p_factor:int) -> None:
        super().__init__(field_size,message_length,payload_length,symbol_size)
        self.p = p_factor
        self.p_unity = self.helper.get_nth_unity_root_of_field(p_factor)
        self.generator_set = []

        for index in range(0,p_factor):
            self.generator_set.append(self.return_generalized_generator(index))
        
        # divisibility of n, k and r should be checked
    
    def encode(self,message):
        #input column zu gf element
        #output n - k entries from start 0 remaining k = input
        # idfgt auf output und return
        if len(message) % self.p != 0:
            raise ValueError("length of message needs to be dvisible by p")
        output_message = message
        message_matrix = self.input_arr_to_matrix(message)
        l = self.two_s//self.p
       
        f_values = []
        shift_poly = np.zeros(l+1,dtype=int)
        shift_poly[0] = 1
        for f_index in range(0,self.p):
            f_i = gl.Poly(shift_poly,field=self.galois_field)* gl.Poly(self.helper.fourier_transform(np.transpose(message_matrix),f_index,self.p))
            f_values.append((f_i % self.generator_set[f_index]).coeffs)

        parity_values =[]
        for h_index in range(0,self.p):
            h_i = self.galois_field(self.helper.inverse_fourier_transform(np.transpose(np.array(f_values)),h_index,self.p))
            parity_values.append(h_i)
        
        for parity_value_index in range(0,l):
            for parity_array_index in range(0,self.p):
                output_message.append(int(parity_values[self.p-parity_array_index-1][parity_value_index]))
        
        return output_message
    
    def decode(self, recieved_msg):
        pass
    
    def primitive_element_adjusted(self,index):
        factor_unity = index % self.p
        factor_primitive = divmod(index,self.p)[0]
        return  self.p_unity**factor_unity * self.galois_field.primitive_element**factor_primitive
    
    def return_generalized_generator(self, index):
        if index >= self.p:
            raise ValueError("Generator polynominals can only be generated from 0 to p-1") 
        ## index is first value that qualifies i%self.p == index condition
        output_poly = gl.Poly([1,-self.galois_field.primitive_element**index],self.galois_field)
        ## start looping after index
        for i in range(index+1,self.two_s):
            if i % self.p == index:
                output_poly *= gl.Poly([1,-self.galois_field.primitive_element**i],self.galois_field)
        return output_poly
    
    def input_arr_to_matrix(self,_arr):
        output = []
        p = self.p
        intermediate_arr = []
        for i in range(0,len(_arr)):
            intermediate_arr.append(_arr[i])
            if (i+1) % p == 0:
                output.append(intermediate_arr[::-1])
                intermediate_arr = []
        return np.array(np.transpose(output))