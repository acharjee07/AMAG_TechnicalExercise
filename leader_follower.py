
import pandas as pd
import math
from utils import haversine_dist,get_angle
import argparse


def find_leader(obj1_cord,obj2_cord):
    """ finds the leader by applying some vector analogy,
    input geo cordinate is in shape (latitude and longitude) of two timestamps
    input:(((obj1 time1 lat,obj1 time1 long),(obj1 time2 lat,obj1 time2 long)),((obj2 time1 lat,obj2 time1 long),(obj2 time2 lat,obj2 time2 long)))

    output: "No vehicle moved" or "Vehicles moving opposite" or "Second vehicle" or "First vehicle"
    """

    if haversine_dist(obj1_cord[0],obj1_cord[1])==0 and haversine_dist(obj2_cord[0],obj2_cord[1])==0:
        return 'No vehicle moved'
    elif  get_angle(obj1_cord,obj2_cord) >90:
        return 'Vehicles moving opposite'
    elif haversine_dist(obj1_cord[0],obj2_cord[1])>haversine_dist(obj2_cord[0],obj1_cord[1]):
        return 'Second vehicle'
    else :
        return 'First vehicle'


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
                                (get_cords(traj2,overlapped_timestamps[i]),get_cords(traj2,overlapped_timestamps[i+1])))
        leader_list.append([overlapped_timestamps[i],leader_obj])
    return pd.DataFrame(leader_list,columns=['overlapped time', 'Leader'])


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('trajectory1')
    parser.add_argument('trajectory2')
    args=parser.parse_args()
    trag1=pd.read_csv(args.trajectory1)
    trag2=pd.read_csv(args.trajectory2)

    print(find_leader_full_data(trag1,trag2))



    
    
    








