import unittest
from trajectory_processor import TrajectoryProcessor
import pandas as pd

processor=TrajectoryProcessor()
result_str_dict=processor.result_str_dict

class TestProcessor(unittest.TestCase):
    
    def test_get_leader_single_timestamp(self):
        
             
        #test cases for no vehicle moved        
        self.assertEqual(processor.get_leader_single_timestamp(((0,0),(0,0)),((10,10),(10,10))),result_str_dict[0])
        self.assertEqual(processor.get_leader_single_timestamp(((10,0),(10,0)),((10,0),(10,0))),result_str_dict[0])
        #test cases for vehicle moving opposite
        self.assertEqual(processor.get_leader_single_timestamp(((10,0),(0,0)),((0,0),(10,0))),result_str_dict[-1])
        self.assertEqual(processor.get_leader_single_timestamp(((10,0),(0,0)),((5,0),(10,0))),result_str_dict[-1])
        self.assertEqual(processor.get_leader_single_timestamp(((0,0),(10,10)),((0,0),(-10,-11))),result_str_dict[-1])
        #test cases for first vehicle leader
        self.assertEqual(processor.get_leader_single_timestamp(((0,0),(10,0)),((-3,0),(8,0))),result_str_dict[1])
        self.assertEqual(processor.get_leader_single_timestamp(((5,5),(10,10)),((0,0),(5,0))),result_str_dict[1])
        #test cases for second vehicle leader
        self.assertEqual(processor.get_leader_single_timestamp(((0,0),(10,10)),((5,5),(0,20))),result_str_dict[2])
        self.assertEqual(processor.get_leader_single_timestamp(((0,0),(10,0)),((0,5),(0,15))),result_str_dict[2])


    def test_get_leader_full_timestamp(self):

     
             
        self.assertEqual(processor.get_leader_full_timestamp(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,-1,0],[1,0,0],[2,1,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[1]],[1,result_str_dict[1]]])

        self.assertEqual(processor.get_leader_full_timestamp(pd.DataFrame([[0,-1,0],[1,5,0],[3,10,0],[4,22,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,7,0],[2,18,0],[3,30,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[2]],[1,result_str_dict[2]]])

        self.assertEqual(processor.get_leader_full_timestamp(pd.DataFrame([[0,0,1],[1,0,2],[3,0,5],[4,0,7]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,0,-1],[2,0,-2],[3,0,-3]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[-1]],[1,result_str_dict[-1]]])

        self.assertEqual(processor.get_leader_full_timestamp(pd.DataFrame([[0,0,0],[1,0,0],[3,0,5],[4,0,7]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,-1],[1,0,-1],[2,0,0],[3,0,3]],columns=['Time (s)','Latitude','Longitude'])),
                                                [[0,result_str_dict[0]],[1,result_str_dict[1]]])


    def test_get_TTC_single_timestamp(self):

        self.assertEqual(processor.get_TTC_single_timestamp(((0,0),(0,0)),((10,10),(10,10)),3),None)
        self.assertEqual(processor.get_TTC_single_timestamp(((0,0),(11,0)),((2,0),(12,0)),3e5),299991.906)
        self.assertEqual(processor.get_TTC_single_timestamp(((10,10),(20,20)),((5,5),(19,19)),3e5),72795.258)
       
    def test_get_TTC_full_timestamp(self):

        self.assertEqual(processor.get_TTC_full_timestamp(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                result_str_dict[3])
        self.assertEqual(processor.get_TTC_full_timestamp(pd.DataFrame([[0,0,0],[1,1,0],[2,2,0]],columns=['Time (s)','Latitude','Longitude']),
                                                pd.DataFrame([[0,-1,0],[1,1.5,0],[2,1,0]],columns=['Time (s)','Latitude','Longitude'])),
                                                (0.333,1))
        
        

if __name__=='__main__':
    unittest.main()