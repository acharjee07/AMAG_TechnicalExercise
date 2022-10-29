
import pandas as pd
import math
from utils import haversine_dist,get_angle









def find_leader(obj1_cord,obj2_cord):

    ''' finds the leader by applying some vector analogy,
    input geo cordinate is in shape (latitude and longitude) of two timestamps
    input=(((obj1 time1 lat,obj1 time1 long),(obj1 time2 lat,obj1 time2 long)),((obj2 time1 lat,obj2 time1 long),(obj2 time2 lat,obj2 time2 long)))
    '''

    

    dis_1_2=haversine_dist(obj1_cord[0],obj2_cord[1])
    dis_2_1=haversine_dist(obj2_cord[0],obj1_cord[1])

    dist_1_1=haversine_dist(obj1_cord[0],obj1_cord[1])
    dist_2_2=haversine_dist(obj2_cord[0],obj2_cord[1])


    if get_angle(obj1_cord,obj2_cord) >90:
        return 'vehicles moving opposite'
    elif dis_1_2>dis_2_1:
        return 'second vehicle'

    elif dist_1_1==0 and dist_2_2==0:
        return 'No vehicle moved'
    else :
        return 'first vehicle'



def find_leader_full_data(trag1,trag2):
    ''' input is two tragentroy as pandas dataframe format format
        output is which one is the leader as a dataframe fromat'''

    tr1_time=trag1['Time (s)']
    tr2_time=trag2['Time (s)']

    overlapped_timestamps=list(set(list(tr1_time)).intersection(list(tr2_time)))

    overlapped_timestamps.sort()
 
    leader_list=[]
    for i in range(len(overlapped_timestamps)-1):
        
        obj1_t1=(trag1[trag1['Time (s)']==overlapped_timestamps[i]]['Latitude'].values[0],trag1[trag1['Time (s)']==overlapped_timestamps[i]]['Longitude'].values[0])
        obj2_t1=(trag2[trag2['Time (s)']==overlapped_timestamps[i]]['Latitude'].values[0],trag2[trag2['Time (s)']==overlapped_timestamps[i]]['Longitude'].values[0])

        obj1_t2=(trag1[trag1['Time (s)']==overlapped_timestamps[i+1]]['Latitude'].values[0],trag1[trag1['Time (s)']==overlapped_timestamps[i+1]]['Longitude'].values[0])
        obj2_t2=(trag2[trag2['Time (s)']==overlapped_timestamps[i+1]]['Latitude'].values[0],trag2[trag2['Time (s)']==overlapped_timestamps[i+1]]['Longitude'].values[0])

        
        leader_obj=find_leader((obj1_t1,obj1_t2),(obj2_t1,obj2_t2))
        leader_list.append([overlapped_timestamps[i],leader_obj])
    return pd.DataFrame(leader_list,columns=['overlapped time', 'Leader'])









import argparse
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('trajectory1')
    parser.add_argument('trajectory2')
    args=parser.parse_args()
    trag1=pd.read_csv(args.trajectory1)
    trag2=pd.read_csv(args.trajectory2)

    print(find_leader_full_data(trag1,trag2))



    
    
    









# print(trag1)
# print(trag2)

# print(find_leader_full_data(trag1,trag2))







# test_cases=[{'input':[((23.726063, 90.391530),(23.725914, 90.391669)),((23.726171, 90.391135),(23.726061, 90.391414))], 'output':1},
            
            
#             ]

# for case in test_cases:
#     if  find_leader(case['input'][0],case['input'][1])==case['output']:
#         print('successful')
#     else:
#         print('error')
#         print(case)
#         print(find_leader(case['input'][0],case['input'][1]))