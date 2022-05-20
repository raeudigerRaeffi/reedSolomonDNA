from dataclasses import field
from msilib.schema import Error
from re import S
import numpy as np
import galois as gl
from . import basereedsolomon




class Generalized_Reed_Solomon(basereedsolomon.Base_Reed_Solomon):

    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int,p_factor:int,irr_poly=None) -> None:
        super().__init__(field_size,message_length,payload_length,symbol_size,irr_poly)    
        self.p = p_factor
        self.primitive = self.galois_field.primitive_element #gl.primitive_root(1)
            
        print("get unity root")
        self.p_unity = self.helper.get_nth_unity_root_of_field(p_factor)
        self.generator_set = []

        ## handles cases where either k or r are not divisible by p, implies by extension the n may not be divisible by p
        self.d = self.two_s % self.p #remainder of r
        self.c = self.payload_length % self.p #remainder of k
        self.num_of_padded_zeros =  (self.p - self.c) if self.c != 0 else 0
        """
        self.payload_length_orignal = self.payload_length
        self.message_length_original = self.message_length
        self.two_s_original = self.two_s
        
        #case 1
        if self.c != 0  and self.d == 0:
            self.payload_length = self.payload_length + self.num_of_padded_zeros
            self.message_length = self.message_length + self.num_of_padded_zeros
        """
        #adjust parameters to handle r not divisble by p
        """if self.d != 0:
            self.payload_length = self.payload_length_orignal + (self.p - self.c)
            self.two_s = self.two_s + (self.p - self.d)
            self.message_length = + self.message_length + (self.p - self.c)
            print("la matrix",self.calculate_t_matrix())
            print("le matrix",np.linalg.inv(self.calculate_v_matrix()))
            print("la le matrix",np.dot(self.calculate_t_matrix() ,np.linalg.inv(self.calculate_v_matrix())))
        """
        for index in range(0,p_factor):
            print("init generator:",index)
            g_i = self.return_generalized_generator(index)
            print("roots",g_i)
            self.generator_set.append(g_i)
        
        
        # divisibility of n, k and r should be checked
    
    def encode(self,message):
        if len(message) != self.payload_length:
            raise("Length not as specified")
        print(message)

        if self.c != 0 and self.d == 0:
            # add conceptual zeros
            message = message +([0]*self.num_of_padded_zeros)
            msg = self.encode_classic(message)
            #remove conceptual zeros
            msg = msg[0:self.payload_length] + msg[self.payload_length + self.num_of_padded_zeros:len(msg)]
            return msg
        if self.d != 0:
            message = message +([0]*self.num_of_padded_zeros)
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
           # recieved_msg = recieved_msg[0:self.payload_length] +([0]*self.num_of_padded_zeros) + recieved_msg[self.payload_length:len(recieved_msg)]
            print("bef", recieved_msg)
            print("p1",recieved_msg[0:self.payload_length])
            print("p2",recieved_msg[self.payload_length:len(recieved_msg)])
            recieved_msg =  recieved_msg[0:self.payload_length] +([0]*self.num_of_padded_zeros) + recieved_msg[self.payload_length:len(recieved_msg)]
            corrected_msg = self.decode_classic(recieved_msg)
            corrected_msg = corrected_msg[0:self.payload_length] + corrected_msg[self.payload_length:len(corrected_msg)]
            return self.return_info_symbols(corrected_msg)

        if self.d != 0:
            recieved_msg =   ([0] * (self.p-self.c))+ recieved_msg
            corrected_msg = self.decode_classic(recieved_msg)
            print("corre",corrected_msg)
            return self.return_info_symbols(corrected_msg)
        
        corrected_msg = self.decode_classic(recieved_msg)
        print("dec internal",corrected_msg)
        return self.return_info_symbols(corrected_msg)

    def encode_classic(self,message):
        #TODO ass case for if k, r or n are not dovisible by p

        output_message = message
        message_matrix = self.input_arr_to_matrix(message)
        l = self.two_s//self.p
        print("messgae matrix before",message_matrix)
        #performs shift by x**l
        temp_message_matrix = []
        for row_id in  range(0,message_matrix.shape[0]):
            msg_slice = np.copy(message_matrix[row_id])
            msg_slice = np.append(msg_slice,np.zeros(l, dtype = int)) #l+1 in case of r not divisible gets handled by the zeros added before encoding
            print("msg_slice_poly",gl.Poly(msg_slice,field=self.galois_field))
            temp_message_matrix.append(msg_slice)
        message_matrix = np.array(temp_message_matrix)
        print("messgae matrix after",message_matrix)
        f_values = []

        fft = self.helper.fft_on_matrix(message_matrix)
        for f_index in range(0,self.p):
            f_i = gl.Poly(fft[f_index],field=self.galois_field)
            print("fi",f_i,fft[f_index],f_i% self.generator_set[f_index] )
            f_values.append((f_i % self.generator_set[f_index]).coeffs)

        parity_values =[]
        
        print("fft",self.galois_field(fft))
        print("fvalue",f_values)

        #f_values = self.galois_field([[30, 27,  5], [ 10, 12, 29],[28,28,9]]) #TODO remove asqap jsut to test a special case

        ifft = self.helper.ifft_on_matrix(f_values)
        print("ifft",ifft)
        for h_index in range(0,self.p):
            h_i = ifft[h_index]
            parity_values.append(h_i)
        
        for parity_value_index in range(0,l):
            for parity_array_index in range(0,self.p):
                output_message.append(int(parity_values[self.p-parity_array_index-1][parity_value_index]))
        
        return output_message
    
    def decode_classic(self, recieved_msg):
        ## TODO add sanity check that length is correct
        syndromes = self.calc_syndrome(recieved_msg)
        #TODO if all syndromes are 0 stop
        print("syndromes",syndromes)
        galois_lfsr = gl.berlekamp_massey(self.galois_field(syndromes),"galois")
        error_locator_polynominal = galois_lfsr.feedback_poly
        error_evaluator_polynominal = gl.Poly(galois_lfsr.state,field =self.galois_field)
        print("berlekamp",galois_lfsr)
        print("berlekamp minimal", gl.berlekamp_massey(self.galois_field(syndromes)))
        print("degree error",error_locator_polynominal.coeffs)
        
        
        #TODO get degree of error locator polynominal if v > n-k/2 abort
        error_locations = self.modified_chien_search(error_locator_polynominal.coeffs[::-1])
        error_locations_index = [(self.message_length + self.num_of_padded_zeros)- x-1 for x in error_locations] #need to be len(recived msg -1 - location)
        print("err_loc",error_locations,len(syndromes))
        
        error_magnitude = self.modified_forney(error_locator_polynominal,error_evaluator_polynominal,error_locations)
        print("err mag",error_magnitude)
        correction_msg = self.galois_field([0]* len(recieved_msg))
        for index in range(0,len(error_locations_index)):
            correction_msg[error_locations_index[index]]  = error_magnitude[index]

        print("err",error_locations)
        print(len(recieved_msg))
        print(self.message_length)
        print(self.num_of_padded_zeros)
        return [ int(symbol) for symbol in (self.galois_field(recieved_msg) + correction_msg)]
    

    def primitive_element_adjusted(self,index):
        factor_unity = index % self.p
        factor_primitive = divmod(index,self.p)[0]
        return  self.p_unity**factor_unity * self.primitive**factor_primitive
    
    def return_generalized_generator(self, index):
        if index >= self.p:
            raise ValueError("Generator polynominals can only be generated from 0 to p-1") 
        ## index is first value that qualifies i%self.p == index condition
        output_poly = gl.Poly([1,-self.primitive**index],field=self.galois_field)
        ## start looping after index
        for i in range(index+1,self.two_s):
            if i % self.p == index:
                output_poly *= gl.Poly([1,-self.primitive**i],field=self.galois_field)
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
        m = len(recieved_codeword)// self.p
        print("rec1",recieved_codeword,len(recieved_codeword))
        print("rec",self.galois_field(recieved_codeword),m)
        #m = len(recieved_codeword) // self.p
        divided_codeword =[]
        for l_index in range(0,self.p):
            syndrome = []
            for m_index in range(0,m):
                recieved_code_index = self.p * m_index + l_index
                syndrome.append(recieved_codeword[len(recieved_codeword)-recieved_code_index -1])
            divided_codeword.append(syndrome[::-1])
        
        fourier_transformed_syndromes = []
        print("div codeword",divided_codeword)
        fft = self.helper.fft_on_matrix(self.galois_field(divided_codeword))
        print("fft_decode",self.galois_field( fft))
        for F_i in range(0,self.p):
            fourier_transformed_syndromes.append(fft[F_i])

        for s_i in range(0,self.two_s):
            primitive_root = self.primitive ** s_i 
            fourier_poly = gl.Poly(fourier_transformed_syndromes[s_i % self.p],field=self.galois_field)
            print("dec fourier_poly", fourier_poly,primitive_root)
            output_syndromes.append(fourier_poly(primitive_root))
            print("s_i",s_i,s_i % self.p,primitive_root,fourier_poly(primitive_root))
        

        return output_syndromes
    
    # modified version for parallelization
    def modified_chien_search(self,error_locator_poly):
        error_locations = []
        
        m = (self.message_length +self.num_of_padded_zeros )// self.p #TODO probably fix with org
        for i in range(0,m):
            modified_a_values = []
            for a_index in range(0,self.p):
                a_i = self.galois_field(0)
                for j_ai_index in range(0,len(error_locator_poly)): ## range v = len error_locator_poly
                    if j_ai_index % self.p == a_index:
                        a_i = a_i + error_locator_poly[j_ai_index] * self.primitive **-(j_ai_index*i) ##TODO check if adjusted primitive is needed
                modified_a_values.append(a_i)
            ifft = np.fft.ifft(self.galois_field(modified_a_values)) #self.helper.ifft_on_matrix(np.array(modified_a_values).T)
            print("moda",modified_a_values)
            print("ifft_dec",ifft)
            for w_index in range(0,self.p):     
                if ifft[w_index] == self.galois_field(0):
                    error_locations.append(self.p * i + w_index)
        return error_locations

    def modified_forney(self,error_location_poly,error_evaluator_poly,error_loc):
        error_magnitudes = []
        for r in error_loc:
            a_i = self.primitive_element_adjusted(r)
            
            error_magnitudes.append( ( a_i * error_evaluator_poly(a_i**-1))/error_location_poly.derivative()(a_i**-1))
        return error_magnitudes
        


    def get_original_msg_slice(self,msg):
        return msg[self.num_of_padded_zeros:self.message_length - self.d -1 ]

    def return_info_symbols(self,msg):
        return msg[0:self.payload_length]
    

    def calculate_t_matrix(self):
        matrix = []
        for i in range(self.d,self.p):
            row = [1]
            for j in range(1,self.d):
                row.append(self.p_unity**(j * i))
            matrix.append(row)
        return self.galois_field(np.matrix(matrix))
    
    def calculate_v_matrix(self):
        matrix = []
        print(self.p_unity,self.p_unity^2)
        matrix.append([1] * self.d)
        for i in range(1,self.d ):
            row = [1]
            for j in range(1,self.d):
                print(self.p_unity^(j*i),j*i)
                row.append(self.p_unity**(j*i))
            matrix.append(row)
        return self.galois_field(np.matrix(matrix))
    
    