import galois as gl
from .helper import Galois_Helper

class Base_Reed_Solomon():
    def __init__(self, field_size:int, message_length:int, payload_length:int,symbol_size:int):
        self.field_size = field_size
        self.galois_field = gl.GF(field_size**symbol_size,display="power")
        self.message_length = message_length
        self.payload_length = payload_length
        self.two_s = message_length - payload_length
        self.helper = Galois_Helper(self.galois_field)