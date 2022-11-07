import unittest
from TTC import get_TTC, get_TTC_fulldata
from leader_follower import result_str_dict
import pandas as pd

class TestCalc(unittest.TestCase):

    def test_get_TTC(self):

        self.assertEqual(get_TTC(((0,0),(0,0)),((10,10),(10,10)),3),None)
        self.assertEqual(get_TTC(((0,0),(11,0)),((2,0),(12,0)),3e5),299991.906)
        self.assertEqual(get_TTC(((10,10),(20,20)),((5,5),(19,19)),3e5),72795.258)
       
    def test_get_TTC_fulldata(self):

        self.assertEqual(get_TTC_fulldata(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                result_str_dict[3])
        self.assertEqual(get_TTC_fulldata(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,-1,0],[1,1.5,0],[2,1,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                (0.333,1))
        
        
        

if __name__=='__main__':
    unittest.main()