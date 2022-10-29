import math
def haversine_dist(c1, c2):
    '''  input is cordinate of two points as tuple (longitude, latitude)
         output is the distance in meters between the two points '''
    
    lat1 ,lon1= c1
    lat2 ,lon2= c2

    R = 6371000  #### radius of earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)


    del_lat = math.radians(lat2 - lat1)
    del_long = math.radians(lon2 - lon1)

    a = math.sin(del_lat / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(del_long / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
   

    meters = round(meters, 3)
  


    # print(f"Distance: {meters} m")

    return meters
   





# test_cases=[{'input':((0,0),(90,0)),'output':(6371000*math.pi/2)},
#             {'input':((0,0),(0,0)),'output':(0)},
#             {'input':((-10,0),(-10,0)),'output':(0)}]


# for case in test_cases:
#     if haversine_dist(case['input'][0],case['input'][1])==round(case['output'],3):
#         print('ok')

#     else:
#          print(case)

# print(haversine_dist((-27.944591900000002, 153.3808251), (-27.93454934, 153.3911746)))





import numpy as np

def get_cartesian(cord):
    """ converts the geo cordinate to cartesian coordinate centering at the center of earth"""
    lat,lon=cord
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    return np.array([x,y,z])
def get_angle(obj1_cord,obj2_cord):
    """ determines the angel btween two vector given the starting and ending coordinate of the vectors"""
    
    vec1_1=get_cartesian(obj1_cord[0])
    vec1_2=get_cartesian(obj1_cord[1])

    vec2_1=get_cartesian(obj2_cord[0])
    vec2_2=get_cartesian(obj2_cord[1])

    vec1=vec1_2-vec1_1
    vec2=vec2_2-vec2_1

    angle=(np.arccos((np.dot(vec1,vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))*180/np.pi)
    return angle