from utils import haversine_dist
from leader_follower import find_leader
import pandas as pd




def get_TTC(obj1_cord,obj2_cord,time):

    obj1_t1=obj1_cord[0]
    obj1_t2=obj1_cord[1]
    obj2_t1=obj2_cord[0]
    obj2_t2=obj2_cord[1]


    leader_obj=find_leader((obj1_t1,obj1_t2),(obj2_t1,obj2_t2))


    xij=haversine_dist(obj1_t2,obj2_t2)
    dis_traveled_obj1=haversine_dist(obj1_t1,obj1_t2)
    dis_traveled_obj2=haversine_dist(obj2_t1,obj2_t2)

    speed_obj1=dis_traveled_obj1/time
    speed_obj2=dis_traveled_obj2/time

    


    if leader_obj=='second vehicle':
        vl=speed_obj2
        vf=speed_obj1
        if (vf-vl)<=0:
            TTC='TTC not applicable'
        else:
            TTC=(xij-3)/(vf-vl)
    
        
    elif leader_obj=='first vehicle':
        vl=speed_obj1
        vf=speed_obj2

        if (vf-vl)<=0:
            TTC='TTC not applicable'
        else:
            TTC=(xij-3)/(vf-vl)

     
        
    
    else: 
        TTC='TTC not applicable'

    return TTC











def get_TTC_fulldata(trag1,trag2):
    tr1_time=trag1['Time (s)']
    tr2_time=trag2['Time (s)']

    overlapped_timestamps=list(set(list(tr1_time)).intersection(list(tr2_time)))

    overlapped_timestamps.sort()

    TTC_list=[]
    for i in range(1,len(overlapped_timestamps)-1):
        
        

        obj1_t1=(trag1[trag1['Time (s)']==overlapped_timestamps[i-1]]['Latitude'].values[0],trag1[trag1['Time (s)']==overlapped_timestamps[i-1]]['Longitude'].values[0])
        obj2_t1=(trag2[trag2['Time (s)']==overlapped_timestamps[i-1]]['Latitude'].values[0],trag2[trag2['Time (s)']==overlapped_timestamps[i-1]]['Longitude'].values[0])

        obj1_t2=(trag1[trag1['Time (s)']==overlapped_timestamps[i]]['Latitude'].values[0],trag1[trag1['Time (s)']==overlapped_timestamps[i]]['Longitude'].values[0])
        obj2_t2=(trag2[trag2['Time (s)']==overlapped_timestamps[i]]['Latitude'].values[0],trag2[trag2['Time (s)']==overlapped_timestamps[i]]['Longitude'].values[0])

        



        
        TTC=get_TTC((obj1_t1,obj1_t2),(obj2_t1,obj2_t2),overlapped_timestamps[i]-overlapped_timestamps[i-1])

        
        
        TTC_list.append([overlapped_timestamps[i],TTC])

    return pd.DataFrame(TTC_list,columns=['TIme','TTC'])





# trag1=pd.read_csv('data/T1.csv')
# trag2=pd.read_csv('data/T2_2.csv')
        

# print(trag1)
# print(trag2)

# print(get_TTC_fulldata(trag1,trag2))



import argparse
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('trajectory1')
    parser.add_argument('trajectory2')
    args=parser.parse_args()
    trag1=pd.read_csv(args.trajectory1)
    trag2=pd.read_csv(args.trajectory2)

    print(get_TTC_fulldata(trag1,trag2))