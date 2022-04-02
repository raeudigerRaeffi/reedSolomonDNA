import galois as gl
import numpy as np

class Galois_Helper():

    def __init__(self,_field) -> None:
        self.field = _field


    ## inefficent should be replaced once libary offers the functionality
    def get_power_of_field_element(self,el):
        divider = self.field.primitive_element
        i = 1
        while int(el/divider) != 1:
            i+= 1
            divider *= self.field.primitive_element
        
        return i

    def get_nth_unity_root_of_field(self,n):
        power_of_one = self.get_power_of_field_element(self.field(1))
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
    
        return self.find_negative_element(self.field(1)/self.field(p)) * np.sum(self.field(array_p_multplier) * self.field(matrix),axis=1)

    def find_negative_element(self,el):
        return self.field((self.field.characteristic**self.field.degree)-1) -el
