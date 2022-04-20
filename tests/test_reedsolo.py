import unittest
import reedSolomon
from reedSolomon import Generalized_Reed_Solomon
import numpy as np


class ReedSoloTest(unittest.TestCase):

    #Test case in which both k and r are divisble by a parameter p
    def test_k_and_r_divisble_by_p(self):
        test_normal_rs = Generalized_Reed_Solomon(2,12,6,4,3)
        normal_msg = test_normal_rs.encode([ 5, 6, 4, 10,3,5])
        normal_msg_org = np.copy(normal_msg)
        normal_msg[2] = 11
        dec_test_normal = test_normal_rs.decode(normal_msg)
        self.assertTrue([ 5, 6, 4, 10,3,5] == dec_test_normal)

    #Test case in which k is not divisble by p but r is
    def test_k_not_divisble_by_p(self):
        inner_encoder = reedSolomon.Generalized_Reed_Solomon(2,11,5,4,3) #n 12 k 5 c 2 r 7 d 1 -> 5 + 9 - (3 -1)
        # 3- 2 = 1   12 -3- 2 = 7 3-1 = 2
        msg = inner_encoder.encode([ 5, 6, 4, 10,3])
        msg_org = np.copy(msg)
        msg[2] = 11
        dec_msg = inner_encoder.decode(msg)
        self.assertTrue([ 5, 6, 4, 10,3] == dec_msg)

if __name__ == '__main__':
    unittest.main()