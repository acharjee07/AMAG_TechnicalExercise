
import pandas as pd
from utils import CoordinateProcessor
import argparse





class TrajectoryProcessor():
    def __init__(self):
        self.result_str_dict={
    -1: 'Vehicles moving opposite',
     0: 'No vehicle moved',
     1: 'First vehicle',
     2: 'Second vehicle',
     3: " Minimum TTC is not applicable for the trajectories"
}


    def get_leader_single_timestamp(self,veh1_cord,veh2_cord):
        """ finds the leader by applying some vector analogy,
        input geo cordinate is in shape (latitude and longitude) of two timestamps
        input:(((veh1 time1 lat,veh1 time1 long),(veh1 time2 lat,veh1 time2 long)),((veh2 time1 lat,veh2 time1 long),(veh2 time2 lat,veh2 time2 long)))

        output: "No vehicle moved" or "Vehicles moving opposite" or "Second vehicle" or "First vehicle"
        """

        if CoordinateProcessor().haversine_dist(veh1_cord[0],veh1_cord[1])==0 and CoordinateProcessor().haversine_dist(veh2_cord[0],veh2_cord[1])==0:
            return self.result_str_dict[0]
        elif  CoordinateProcessor().get_angle(veh1_cord,veh2_cord) >90:
            return self.result_str_dict[-1]
        elif CoordinateProcessor().haversine_dist(veh1_cord[0],veh2_cord[1])>CoordinateProcessor().haversine_dist(veh2_cord[0],veh1_cord[1]):
            return self.result_str_dict[2]
        else :
            return self.result_str_dict[1]


    def get_cords(self,trag,time):
        """ returns the longitude and latitude from a dataframe given the timestamp 
            input: tragectory :in a pandas dataframe format, time: time in seconds
            output:(latitude,longitude) """
        return (trag[trag['Time (s)']==time]['Latitude'].values[0],trag[trag['Time (s)']==time]['Longitude'].values[0])


    def get_leader_full_timestamp(self,traj1,traj2):
        """ input: is two tragentroy as pandas dataframe format 
            returns: is which one is the leader as a dataframe"""

        overlapped_timestamps=list(set(list(traj1['Time (s)'])).intersection(list(traj2['Time (s)'])))
        overlapped_timestamps.sort()
        leader_list=[]
        for i in range(len(overlapped_timestamps)-1):

            leader_obj=self.get_leader_single_timestamp((self.get_cords(traj1,overlapped_timestamps[i]),self.get_cords(traj1,overlapped_timestamps[i+1])),
                                    (self.get_cords(traj2,overlapped_timestamps[i]),self.get_cords(traj2,overlapped_timestamps[i+1]))
                                    )
            leader_list.append([overlapped_timestamps[i],leader_obj])
        return leader_list

    def get_TTC_single_timestamp(self,obj1_cord,obj2_cord,time):
        """
        input:obj1_cord: ((obj1 time1 lat,obj1 time1 long),(obj1 time2 lat,obj1 time2 long)), obj2_cord: ((obj2 time1 lat,obj2 time1 long),(obj2 time2 lat,obj2 time2 long)),
            time: difference in time
        
        output:   TTC if TTC is applicable in the case where TTC not applicable returns None
        
        """
        leader_vehicle=self.get_leader_single_timestamp((obj1_cord[0],obj1_cord[1]),( obj2_cord[0], obj2_cord[1]))
        xij=CoordinateProcessor().haversine_dist(obj1_cord[1], obj2_cord[1])
        dis_traveled_obj1=CoordinateProcessor().haversine_dist(obj1_cord[0],obj1_cord[1])
        dis_traveled_obj2=CoordinateProcessor().haversine_dist(  obj2_cord[0],obj2_cord[1])
        speed_obj1=dis_traveled_obj1/time
        speed_obj2=dis_traveled_obj2/time

        TTC=None
        if leader_vehicle==self.result_str_dict[2]:
            speed_diff=speed_obj1-speed_obj2
            if speed_diff>0:
                TTC=round((xij-3)/speed_diff,3)
        elif leader_vehicle==self.result_str_dict[1]:
            speed_diff=speed_obj2-speed_obj1
            if speed_diff>0:
                TTC=round((xij-3)/speed_diff,3)
        return TTC


    def get_TTC_full_timestamp(self,trag1,trag2):
        """ gets ttc for the whole trajectories, given the trajectories in pandas dataframe format and returns the minimum TTC and the corresponding timestamp"""
        overlapped_timestamps=list(set(list(trag1['Time (s)'])).intersection(list(trag2['Time (s)'])))      
        overlapped_timestamps.sort()
        TTC_list=[]

        ## ttc for the first time stap can not be calculated as the velocity can not be determined
        for i in range(1,len(overlapped_timestamps)):        
            TTC=self.get_TTC_single_timestamp((self.get_cords(trag1,overlapped_timestamps[i-1]),self.get_cords(trag1,overlapped_timestamps[i])),
                    (self.get_cords(trag2,overlapped_timestamps[i-1]),self.get_cords(trag2,overlapped_timestamps[i])),
                    overlapped_timestamps[i]-overlapped_timestamps[i-1])

            TTC_list.append([overlapped_timestamps[i],TTC])

        TTC_df=pd.DataFrame(TTC_list,columns=['Time','TTC']).dropna()

        # after removing all the nan valuse if no TTC is left then minimum ttc is not applicable
        if len(TTC_df)==0:                                  
            return self.result_str_dict[3]
        
        else:
            min_TTC=min(TTC_df['TTC'])
            min_TTC_time=TTC_df[TTC_df['TTC']==min_TTC]['Time'].values[0]
            return min_TTC, min_TTC_time






if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('trajectory1')
    parser.add_argument('trajectory2')
    args=parser.parse_args()
    trag1=pd.read_csv(args.trajectory1)
    trag2=pd.read_csv(args.trajectory2)
    
  

    processor=TrajectoryProcessor()

    print(pd.DataFrame(processor.get_leader_full_timestamp(trag1,trag2),columns=['overlapped time', 'Leader']), '\n')
    
    min_TTC, min_TTC_time=processor.get_TTC_full_timestamp(trag1,trag2)
    print(f'Minimum TTC is {min_TTC} at time {min_TTC_time}s')
    



    
    
    








