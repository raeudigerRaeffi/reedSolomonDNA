from dataclasses import field
import numpy as np
import galois as gl
from .basereedsolomon import Base_Reed_Solomon




class Generalized_Reed_Solomon(Base_Reed_Solomon):
    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int,p_factor:int,irr_poly=None) -> None:
        super().__init__(field_size,message_length,payload_length,symbol_size,irr_poly)
        self.p = p_factor
        print("get unity root")
        self.p_unity = self.helper.get_nth_unity_root_of_field(p_factor)
        self.generator_set = []

        for index in range(0,p_factor):
            print("init generator:",index)
            self.generator_set.append(self.return_generalized_generator(index))
        
        # divisibility of n, k and r should be checked
    
    def encode(self,message):
        #TODO ass case for if k, r or n are not dovisible by p


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
            f_i = gl.Poly(shift_poly,field=self.galois_field)* gl.Poly(self.helper.fourier_transform(np.transpose(message_matrix),f_index,self.p),field=self.galois_field)
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

        syndromes = self.calc_syndrome(recieved_msg)

        galois_lfsr = gl.berlekamp_massey(self.galois_field(syndromes),"galois")
        error_locator_polynominal = galois_lfsr.feedback_poly
        error_evaluator_polynominal = gl.Poly(galois_lfsr.state,field =self.galois_field)

        error_locations = self.modified_chien_search(error_locator_polynominal.coeffs[::-1])
        error_locations_index = [self.message_length- x-1 for x in error_locations] #need to be len(recived msg -1 - location)

        error_magnitude = self.modified_forney(error_locator_polynominal,error_evaluator_polynominal,error_locations)
        correction_msg = self.galois_field([0]*self.message_length)
        for index in range(0,len(error_locations_index)):
            correction_msg[error_locations_index[index]]  = error_magnitude[index]

        return [ int(symbol) for symbol in (self.galois_field(recieved_msg) + correction_msg)]
    
    def primitive_element_adjusted(self,index):
        factor_unity = index % self.p
        factor_primitive = divmod(index,self.p)[0]
        return  self.p_unity**factor_unity * self.galois_field.primitive_element**factor_primitive
    
    def return_generalized_generator(self, index):
        if index >= self.p:
            raise ValueError("Generator polynominals can only be generated from 0 to p-1") 
        ## index is first value that qualifies i%self.p == index condition
        output_poly = gl.Poly([1,-self.galois_field.primitive_element**index],field=self.galois_field)
        ## start looping after index
        for i in range(index+1,self.two_s):
            if i % self.p == index:
                output_poly *= gl.Poly([1,-self.galois_field.primitive_element**i],field=self.galois_field)
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

    
    def calc_syndrome(self,recieved_codeword):
        output_syndromes = []
        m = self.message_length // self.p
        divided_codeword =[]
        for l_index in range(0,self.p):
            syndrome = []
            for m_index in range(0,m):
                recieved_code_index = self.p * m_index + l_index
                syndrome.append(recieved_codeword[len(recieved_codeword)-recieved_code_index -1])
            divided_codeword.append(syndrome[::-1])
        
        fourier_transformed_syndromes = []
        for F_i in range(0,self.p):
            fourier_transformed_syndromes.append(self.helper.fourier_transform((np.transpose(np.array(divided_codeword))),F_i,self.p))

        for s_i in range(0,self.two_s):
            primitive_root = self.galois_field.primitive_element ** s_i
            fourier_poly = gl.Poly(fourier_transformed_syndromes[s_i % self.p],field=self.galois_field)
            output_syndromes.append(fourier_poly(primitive_root))


        return output_syndromes
    
    # modified version for parallelization
    def modified_chien_search(self,error_locator_poly):
        error_locations = []
        m = self.message_length // self.p
        for i in range(0,m):
            modified_a_values = []
            for a_index in range(0,self.p):
                a_i = self.galois_field(0)
                for j_ai_index in range(0,self.payload_length//self.p ):
                    if j_ai_index % self.p == a_index:
                        a_i = a_i + error_locator_poly[j_ai_index] * self.galois_field.primitive_element **-(j_ai_index*i)
                modified_a_values.append(a_i)
            for w_index in range(0,self.p):
                w_i = self.galois_field(0)
                for j_wi_index in range(0,self.p):
                    p_factor =  -j_wi_index*w_index
                    w_i = w_i + modified_a_values[j_wi_index] * self.p_unity**p_factor
            
                if w_i == self.galois_field(0):
                    error_locations.append(self.p * i + w_index)
        return error_locations

    def modified_forney(self,error_location_poly,error_evaluator_poly,error_loc):
        error_magnitudes = []
        error_function_denominator = error_location_poly.derivative() * gl.Poly([1,0],field=self.galois_field)

        for r in error_loc:
            a_i = self.primitive_element_adjusted(r)
            error_magnitudes.append(error_evaluator_poly(a_i**-1)/error_function_denominator(a_i**-1))
        return error_magnitudes            