import math
import numpy as np


class CoordinateProcessor():
    

    def haversine_dist(self,c1, c2):
        """ input is cordinate of two points as tuple (longitude, latitude)
            output is the distance in meters between the two points """
        
        lat1 ,lon1= c1
        lat2 ,lon2= c2
        R = 6371000  #### radius of earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        del_lat = math.radians(lat2 - lat1)
        del_long = math.radians(lon2 - lon1)

        a = math.sin(del_lat / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(del_long / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance_in_meters = R * c  # output distance in meters
        distance_in_meters = round(distance_in_meters, 3)
    
        return distance_in_meters
    
    
    def get_cartesian(self,cord):
        """ converts the geo cordinate to cartesian coordinate centering at the center of earth"""
        lat,lon=cord
        lat, lon = np.deg2rad(lat), np.deg2rad(lon)
        R = 6371000 # radius of the earth
        x = R * np.cos(lat) * np.cos(lon)
        y = R * np.cos(lat) * np.sin(lon)
        z = R *np.sin(lat)

        return np.array([x,y,z])


    def get_angle(self,obj1_cord,obj2_cord):
        """ determines the angel btween two vector given the starting and ending coordinate of the vectors"""
        
        vec1_1=self.get_cartesian(obj1_cord[0])
        vec1_2=self.get_cartesian(obj1_cord[1])
        vec2_1=self.get_cartesian(obj2_cord[0])
        vec2_2=self.get_cartesian(obj2_cord[1])

        vec1=vec1_2-vec1_1
        vec2=vec2_2-vec2_1  

        if np.linalg.norm(vec1)*np.linalg.norm(vec2)==0:
            angle=0            # here the angle is not zero if one vehicle angle is not moving there is no logical angle
                                # to ensure the further logic, the angle is assumed to be 0
        else:                  
            angle=(np.arccos(round((np.dot(vec1,vec2))/(np.linalg.norm(vec1)*np.linalg.norm(vec2)),2))*180/np.pi)
        
        return angle

