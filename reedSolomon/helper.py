import galois as gl
import numpy as np

class Galois_Helper():

    def __init__(self,_field) -> None:
        self.field = _field
        self.base_field = gl.Field(_field.characteristic)
        #print("Basefield",self.base_field)
        #print("Extendedfield",self.field)

    ## inefficent should be replaced once libary offers the functionality
    def get_power_of_field_element(self,el): #TODO check if correct
        divider = self.field.primitive_element
        i = 1
        while int(el/divider) != 1:
            i+= 1
            divider *= self.field.primitive_element
        
        return i

    def find_multiplactive_inverse(self,element):
        power_element = self.get_power_of_field_element(element)
        power_of_one = self.get_power_of_field_element(self.field(1))
        print(power_of_one,power_element)
        return self.field.primitive_element**(power_of_one -power_element )

    def get_nth_unity_root_of_field(self,n):
        power_of_one = (self.field.characteristic **self.field.degree)-1 #self.get_power_of_field_element(self.field(1))
        if power_of_one % n != 0:
            raise ValueError("failure in getting nth root") 
        return self.field.primitive_element**(power_of_one//n)
    
    def fourier_transform(self, matrix,index,p):
        pth_root = self.get_nth_unity_root_of_field(p)
        array_p_multplier = []
        for i in range(0,p):
            p_factor =  i*index
            array_p_multplier.append(pth_root**p_factor)

        return np.sum(self.field(array_p_multplier) * self.field(matrix),axis=1)
    
    def inverse_fourier_transform(self, matrix,index,p):
        pth_root = self.get_nth_unity_root_of_field(p)
        array_p_multplier = []
        for i in range(0,p):
            p_factor =  -i*index
            array_p_multplier.append(pth_root**p_factor)
        
        factor = int(self.base_field(1)/ self.base_field(p % self.base_field.characteristic))

        return factor * np.sum(self.field(array_p_multplier) * self.field(matrix),axis=1)

    def find_negative_element(self,el):#TODO check if correct
        return self.field((self.field.characteristic**self.field.degree)-1) -el
    

    ## currently not neededed
    def modified_berlekamp_massey(self,number_of_steps,syndromes):
        error_locator_poly = [gl.Poly([1],field=self.field)]
        error_locator_support_poly = gl.Poly([1],field=self.field)
        error_evaluator_poly = [gl.Poly([0],field=self.field)]
        # x^-1 is ax where ax * x = 1
        error_evaluator_support_poly = gl.Poly(self.find_multiplactive_inverse(self.field("a^1")).vector(),field=self.field)
        L = 0
        #print( gl.Poly([1]))
        #print(gl.Poly([1,0]))
        #print(error_evaluator_poly)
        for k in range(0,number_of_steps):
            discrepancy = gl.Poly([0],field=self.field)
            for i in range(0,L+1):
                # calculate discrepancy 
                discrepancy = discrepancy +error_locator_poly[i] * gl.Poly([syndromes[k-i]],field=self.field)
            # update error locator polys
            error_locator_poly_new = error_locator_poly[k] + (self.find_negative_element(discrepancy) * error_locator_support_poly * gl.Poly([1,0],field=self.field))
            error_evaluator_poly_new = error_evaluator_poly[k]-( discrepancy * error_evaluator_support_poly * gl.Poly([1,0],field=self.field))
            error_evaluator_poly.append(error_evaluator_poly_new )
            error_locator_poly.append(error_locator_poly_new )
            
            if discrepancy != gl.Poly([0],field=self.field) and 2*L <= k:
                error_locator_support_poly = error_locator_poly[k]/discrepancy
            print(error_locator_poly)
            print(error_evaluator_poly)
            print(error_locator_support_poly)
            print(error_evaluator_support_poly * gl.Poly([1,0],field=self.field))
            break
        pass
