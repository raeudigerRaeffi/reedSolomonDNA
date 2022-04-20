from dataclasses import field
from msilib.schema import Error
import numpy as np
import galois as gl
from . import basereedsolomon




class Generalized_Reed_Solomon(basereedsolomon.Base_Reed_Solomon):

    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int,p_factor:int,irr_poly=None) -> None:
        super().__init__(field_size,message_length,payload_length,symbol_size,irr_poly)    
        self.p = p_factor
            
            
        print("get unity root")
        self.p_unity = self.helper.get_nth_unity_root_of_field(p_factor)
        self.generator_set = []

        ## handles cases where either k or r are not divisible by p, implies by extension the n may not be divisible by p
        self.d = self.two_s % self.p #remainder of r
        self.c = self.payload_length % self.p #remainder of k
        self.num_of_padded_zeros =  self.p - self.c
        self.payload_length_orignal = self.payload_length
        self.message_length_original = self.message_length
        #case 1
        if self.c != 0  and self.d == 0:
            self.payload_length = self.payload_length + self.num_of_padded_zeros
            self.message_length = self.message_length + self.num_of_padded_zeros

        #adjust parameters to handle r not divisble by p
        if self.d != 0:
            self.payload_length = self.payload_length_orignal + (self.p - self.c)
            self.two_s = self.two_s + (self.p - self.d)
            self.message_length = + self.payload_length + self.two_s


        for index in range(0,p_factor):
            print("init generator:",index)
            self.generator_set.append(self.return_generalized_generator(index))
        
        
        # divisibility of n, k and r should be checked
    
    def encode(self,message):
        if len(message) != self.payload_length_orignal:
            raise("Length not as specified")
        print(message)

        if self.c != 0 and self.d == 0:
            # add conceptual zeros
            message = message +([0]*self.num_of_padded_zeros)
            msg = self.encode_classic(message)
            #remove conceptual zeros
            msg = msg[0:self.payload_length_orignal] + msg[self.payload_length:len(msg)]
            return msg
        if self.d != 0:
            message = ([0]*self.num_of_padded_zeros) + message
            print(message)
            msg = self.encode_classic(message)
            print("msg",msg)
            msg = self.get_original_msg_slice(msg)
            print("af",msg)
            return msg 

        msg = self.encode_classic(message)            
        return msg

    def decode(self, recieved_msg):

        if self.c != 0 and self.d == 0:
            recieved_msg = recieved_msg[0:self.payload_length] +([0]*self.num_of_padded_zeros) + recieved_msg[self.payload_length:len(recieved_msg)]
            corrected_msg = self.decode_classic(recieved_msg)
            corrected_msg = corrected_msg[0:self.payload_length_orignal] + corrected_msg[self.payload_length:len(corrected_msg)]
            return self.return_info_symbols(corrected_msg)

        if self.d != 0:
            corrected_msg = self.decode_r_not_divisble(recieved_msg)
            print("corre",corrected_msg)
            return self.return_info_symbols(corrected_msg)
        
        corrected_msg = self.decode_classic(recieved_msg)
        return self.return_info_symbols(corrected_msg)

    def encode_classic(self,message):
        #TODO ass case for if k, r or n are not dovisible by p

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
        print(f_values)
        for h_index in range(0,self.p):
            h_i = self.galois_field(self.helper.inverse_fourier_transform(np.transpose(np.array(f_values)),h_index,self.p))
            parity_values.append(h_i)
        
        for parity_value_index in range(0,l):
            for parity_array_index in range(0,self.p):
                output_message.append(int(parity_values[self.p-parity_array_index-1][parity_value_index]))
        
        return output_message
    
    def decode_classic(self, recieved_msg):

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

        print("err",error_locations)
        return [ int(symbol) for symbol in (self.galois_field(recieved_msg) + correction_msg)]
    
    # handles case in which r is not divisble by r
    def decode_r_not_divisble(self,recieved_msg):
        #construct new z message polynominal
        z = [0] * self.message_length
        print(self.galois_field(4) + self.galois_field(11))
        for z_index in range(self.d  ,self.message_length - self.num_of_padded_zeros -1):        
            z[z_index] = int(self.return_adjustment_delta(z_index) * self.galois_field(recieved_msg[z_index - self.num_of_padded_zeros]))

        print("z",z)
        syndromes = self.calc_syndrome(z)
        galois_lfsr = gl.berlekamp_massey(self.galois_field(syndromes),"galois")
        error_locator_polynominal = galois_lfsr.feedback_poly
        error_evaluator_polynominal = gl.Poly(galois_lfsr.state,field =self.galois_field)

        error_locations = self.modified_chien_search(error_locator_polynominal.coeffs[::-1])
        print("err_loc",error_locations)
        error_locations_index = [self.message_length- x-1 for x in error_locations] #need to be len(recived msg -1 - location)
        error_magnitude = self.modified_forney_r_not_divisble(error_locator_polynominal,error_evaluator_polynominal,error_locations)
        correction_msg = self.galois_field([0]*self.message_length)
        for index in range(0,len(error_locations_index)):
            correction_msg[error_locations_index[index]]  = error_magnitude[index]
        
        correction_msg = self.get_original_msg_slice(correction_msg)
        print("corr",correction_msg)
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
        #m = self.message_length // self.p
        m = len(recieved_codeword) // self.p
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
                for j_ai_index in range(0,len(error_locator_poly)): ## range v = len error_locator_poly
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
        
    
    def modified_forney_r_not_divisble(self,error_location_poly,error_evaluator_poly,error_loc):
        error_magnitudes = []
        error_function_denominator = error_location_poly.derivative() * gl.Poly([1,0],field=self.galois_field)
        
        for r in error_loc:
            a_i = self.primitive_element_adjusted(r)
            error_magnitiude =  self.return_adjustment_delta(r) * (error_evaluator_poly(a_i**-1)/error_function_denominator(a_i**-1))
            error_magnitudes.append(error_magnitiude)
        return error_magnitudes

    def get_original_msg_slice(self,msg):
        return msg[self.num_of_padded_zeros:self.message_length - self.d -1 ]

    def return_info_symbols(self,msg):
        return msg[0:self.payload_length_orignal]
    
    #used for case in which r%p != p
    def return_adjustment_delta(self,index):
        term_to_multiply = self.galois_field(1)
        a_i = self.primitive_element_adjusted(index)
        for j_index in range(0,self.p - self.d):
            term_to_multiply = term_to_multiply * (a_i -self.p_unity**j_index)
        return term_to_multiply

    
    