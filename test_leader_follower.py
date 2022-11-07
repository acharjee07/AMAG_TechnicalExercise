import unittest
from leader_follower import find_leader,find_leader_full_data,result_str_dict
import pandas as pd

class TestCalc(unittest.TestCase):

    def test_leader_follower(self):      
        #test cases for no vehicle moved        
        self.assertEqual(find_leader(((0,0),(0,0)),((10,10),(10,10)),result_str_dict),result_str_dict[0])
        self.assertEqual(find_leader(((10,0),(10,0)),((10,0),(10,0)),result_str_dict),result_str_dict[0])
        #test cases for vehicle moving opposite
        self.assertEqual(find_leader(((10,0),(0,0)),((0,0),(10,0)),result_str_dict),result_str_dict[-1])
        self.assertEqual(find_leader(((10,0),(0,0)),((5,0),(10,0)),result_str_dict),result_str_dict[-1])
        self.assertEqual(find_leader(((0,0),(10,10)),((0,0),(-10,-11)),result_str_dict),result_str_dict[-1])
        #test cases for first vehicle leader
        self.assertEqual(find_leader(((0,0),(10,0)),((-3,0),(8,0)),result_str_dict),result_str_dict[1])
        self.assertEqual(find_leader(((5,5),(10,10)),((0,0),(5,0)),result_str_dict),result_str_dict[1])
        #test cases for second vehicle leader
        self.assertEqual(find_leader(((0,0),(10,10)),((5,5),(0,20)),result_str_dict),result_str_dict[2])
        self.assertEqual(find_leader(((0,0),(10,0)),((0,5),(0,15)),result_str_dict),result_str_dict[2])


    def test_find_leader_full_data(self):        
        self.assertEqual(find_leader_full_data(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,-1,0],[1,0,0],[2,1,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[1]],[1,result_str_dict[1]]])

        self.assertEqual(find_leader_full_data(pd.DataFrame([[0,-1,0],[1,5,0],[3,10,0],[4,22,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,7,0],[2,18,0],[3,30,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[2]],[1,result_str_dict[2]]])

        self.assertEqual(find_leader_full_data(pd.DataFrame([[0,0,1],[1,0,2],[3,0,5],[4,0,7]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,0,-1],[2,0,-2],[3,0,-3]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[-1]],[1,result_str_dict[-1]]])

        self.assertEqual(find_leader_full_data(pd.DataFrame([[0,0,0],[1,0,0],[3,0,5],[4,0,7]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,-1],[1,0,-1],[2,0,0],[3,0,3]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[0]],[1,result_str_dict[1]]])
        
        

if __name__=='__main__':
    unittest.main()