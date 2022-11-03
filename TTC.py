from utils import haversine_dist
from leader_follower import find_leader, get_cords
import pandas as pd




def get_TTC(obj1_cord,obj2_cord,time):
    ''' returns ttc for given two consecutive timestamps
    
    input=obj1_cord: ((obj1 time1 lat,obj1 time1 long),(obj1 time2 lat,obj1 time2 long)), obj2_cord: ((obj2 time1 lat,obj2 time1 long),(obj2 time2 lat,obj2 time2 long)),
          time: difference in time
    
    Output= Returns the TTC if TTC is applicable in the case where TTC not applicable returns None
    
    '''




    leader_obj=find_leader((obj1_cord[0],obj1_cord[1]),( obj2_cord[0], obj2_cord[1]))


    xij=haversine_dist(obj1_cord[1], obj2_cord[1])
    dis_traveled_obj1=haversine_dist(obj1_cord[0],obj1_cord[1])
    dis_traveled_obj2=haversine_dist(  obj2_cord[0],obj2_cord[1])

    speed_obj1=dis_traveled_obj1/time
    speed_obj2=dis_traveled_obj2/time

    


    if leader_obj=='Second vehicle':
        vl=speed_obj2
        vf=speed_obj1
        if (vf-vl)<=0:
            TTC=None
        else:
            TTC=(xij-3)/(vf-vl)
    
        
    elif leader_obj=='First vehicle':
        vl=speed_obj1
        vf=speed_obj2

        if (vf-vl)<=0:
            TTC=None
        else:
            TTC=(xij-3)/(vf-vl)

     
        
    
    else: 
        TTC=None

    return TTC











def get_TTC_fulldata(trag1,trag2):
    ''' gets ttc for the whole trajectories, given the trajectories in pandas dataframe format and returns the minimum TTC and the corresponding timestamp'''
    tr1_time=trag1['Time (s)']
    tr2_time=trag2['Time (s)']

    overlapped_timestamps=list(set(list(tr1_time)).intersection(list(tr2_time)))      

    overlapped_timestamps.sort()

    TTC_list=[]
    for i in range(1,len(overlapped_timestamps)):        ## ttc for the first time stap can not be calculated as the velocity can not be determined
        
        
        obj1_t1=get_cords(trag1,overlapped_timestamps[i-1])
        obj2_t1=get_cords(trag2,overlapped_timestamps[i-1])
        obj1_t2=get_cords(trag1,overlapped_timestamps[i])
        obj2_t2=get_cords(trag2,overlapped_timestamps[i])

        
        TTC=get_TTC((obj1_t1,obj1_t2),(obj2_t1,obj2_t2),overlapped_timestamps[i]-overlapped_timestamps[i-1])

        
        
        TTC_list.append([overlapped_timestamps[i],TTC])

    TTC_df=pd.DataFrame(TTC_list,columns=['Time','TTC']).dropna()


    if len(TTC_df)==0:                                  # after removing all the nan valuse if no TTC is left then minimum ttc is not applicable
        return " Minimum TTC is not applicable for the trajectories"
    else:

        min_TTC=min(TTC_df['TTC'])
        min_TTC_time=TTC_df[TTC_df['TTC']==min_TTC]['Time'].values[0]


        return f'Minimum TTC is {min_TTC} at time {min_TTC_time}'





# trag1=pd.read_csv('data/T3.csv')
# trag2=pd.read_csv('data/T4.csv')
        

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