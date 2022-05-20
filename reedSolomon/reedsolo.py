import numpy as np



"""
@param x is a numpy array
@param y is a numpy array
"""

class reedSolo:
    def __init__(self,field_size:int,symbol_size:int,message_length:int,payload_length:int,irreducible_poly) -> None:
        self.field_size = field_size
        self.symbol_size = symbol_size
        self.n = message_length
        self.k = payload_length
        self.s = (message_length - payload_length)/2
        self.irreducible_poly = np.array(irreducible_poly)
    
    """
    @param x is a numpy array
    @param y is a numpy array
    @output numpy array
    """
    def gf_addition(self,x,y):
        if len(x) != len(y):
            raise "arrays must be of same length"
        return (x+y) % self.field_size

    """
    @param x is a numpy array
    @param y is a numpy array
    @output numpy array
    """
    def gf_subtraction(self,x,y):
        if len(x) != len(y):
            raise "arrays must be of same length"
        minus_y = ((y - self.field_size) * -1) % self.field_size
        return (x+minus_y) % self.field_size

    def gf_multiplication(self,x,y):

        """
        Performs polynominal multiplication
        """
        def poly_multiply(x,y):
            ## max length of array is lengths combined minus 1
            output = np.zeros(len(x)+len(y) - 1)
            for i in range(0,len(x)):
                target = np.zeros(i + len(y))
                element_x  = x[i]
                for e in range(0,len(y)):
                    target[i+e] = element_x * y[e]
                target.resize(output.shape) # is this efficent ?
                output = output + target
            return output
        
        polynominals_multiplied = poly_multiply(x,y) % self.field_size
        print(polynominals_multiplied)
        #only return modulo to keep elements in the field
        return self.gf_poly_div(polynominals_multiplied, self.irreducible_poly)["remainder"]

    '''Extended synthetic division for galois polynominals.'''
    def gf_poly_div(self,dividend, divisor):
    
        divider_remainder_list = list(dividend)
        
        for i in range(0, len(dividend) - (len(divisor)-1)):
            coef = divider_remainder_list[i] 
            # 0 values can be ignored
            if coef != 0: 
                #skip first coefficent of division
                for j in range(1, len(divisor)): 
                    #0 values can be ignored
                    if divisor[j] != 0: 
                        divider_remainder_list[i + j] = (divider_remainder_list[i + j] + (divisor[j] * coef)) % self.field_size
                        #divider_remainder_list[i + j] %= 

        # divider_remainder_list has division result and remainder stored
        # seperator to distingush between result and remainder is calculated
        separator = -(len(divisor)-1)
        return {
                "quotient":divider_remainder_list[:separator], 
                "remainder":divider_remainder_list[separator:]
                } 




##Tests
coder = reedSolo(2,8,255,223,[1,0,0,0,1,1,1,0,1])
x = [1,0,0,0,1,0,0,1] 
y = [1,0,1,0,1,0] 
print(coder.gf_multiplication(x,y))