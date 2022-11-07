
import pandas as pd
from utils import haversine_dist,get_angle
import argparse


result_str_dict={
    -1: 'Vehicles moving opposite',
     0: 'No vehicle moved',
     1: 'First vehicle',
     2: 'Second vehicle',
     3: " Minimum TTC is not applicable for the trajectories"
}

def find_leader(veh1_cord,veh2_cord,result_str_dict):
    """ finds the leader by applying some vector analogy,
    input geo cordinate is in shape (latitude and longitude) of two timestamps
    input:(((veh1 time1 lat,veh1 time1 long),(veh1 time2 lat,veh1 time2 long)),((veh2 time1 lat,veh2 time1 long),(veh2 time2 lat,veh2 time2 long)))

    output: "No vehicle moved" or "Vehicles moving opposite" or "Second vehicle" or "First vehicle"
    """

    if haversine_dist(veh1_cord[0],veh1_cord[1])==0 and haversine_dist(veh2_cord[0],veh2_cord[1])==0:
        return result_str_dict[0]
    elif  get_angle(veh1_cord,veh2_cord) >90:
        return result_str_dict[-1]
    elif haversine_dist(veh1_cord[0],veh2_cord[1])>haversine_dist(veh2_cord[0],veh1_cord[1]):
        return result_str_dict[2]
    else :
        return result_str_dict[1]


def get_cords(trag,time):
    """ returns the longitude and latitude from a dataframe given the timestamp 
        input: tragectory :in a pandas dataframe format, time: time in seconds
        output:(latitude,longitude) """
    return (trag[trag['Time (s)']==time]['Latitude'].values[0],trag[trag['Time (s)']==time]['Longitude'].values[0])


def find_leader_full_data(traj1,traj2):
    """ input: is two tragentroy as pandas dataframe format 
        returns: is which one is the leader as a dataframe"""

    overlapped_timestamps=list(set(list(traj1['Time (s)'])).intersection(list(traj2['Time (s)'])))
    overlapped_timestamps.sort()
    leader_list=[]
    for i in range(len(overlapped_timestamps)-1):

        leader_obj=find_leader((get_cords(traj1,overlapped_timestamps[i]),get_cords(traj1,overlapped_timestamps[i+1])),
                                (get_cords(traj2,overlapped_timestamps[i]),get_cords(traj2,overlapped_timestamps[i+1])),
                                result_str_dict)
        leader_list.append([overlapped_timestamps[i],leader_obj])
    return leader_list


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('trajectory1')
    parser.add_argument('trajectory2')
    args=parser.parse_args()
    trag1=pd.read_csv(args.trajectory1)
    trag2=pd.read_csv(args.trajectory2)

    print(pd.DataFrame(find_leader_full_data(trag1,trag2),columns=['overlapped time', 'Leader']))
    



    
    
    








