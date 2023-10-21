import pygame
from  pygame import Vector2
import numpy
from math import cos, sin, asin, sqrt, pi, radians

def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = cos(radians(lat2)) * sin(radians(dLon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(dLon))
    brng = numpy.arctan2(x,y)
    brng = numpy.degrees(brng)

    return brng

def get_distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...


class GpsDisplay:

    def __init__(self,pos,size,start_loc,fov=10):
        self.x, self.y = pos
        self.size = size

        self.start_loc = start_loc
        self.source1_loc = start_loc
        self.source2_loc = start_loc

        self.angle1 = get_bearing(*self.source1_loc,*self.start_loc)
        self.distance1 = get_distance(*self.source1_loc,*self.start_loc)

        self.angle2 = get_bearing(*self.source2_loc,*self.start_loc)
        self.distance2 = get_distance(*self.source2_loc,*self.start_loc)

        self.fov = fov
    
    def set_coordinates(self,source1,source2):
        self.source1_loc, self.source2_loc = source1, source2

        self.angle1 = get_bearing(*self.source1_loc,*self.start_loc)
        self.distance1 = get_distance(*self.source1_loc,*self.start_loc)

        self.angle2 = get_bearing(*self.source2_loc,*self.start_loc)
        self.distance2 = get_distance(*self.source2_loc,*self.start_loc)
    
    def render(self,source):



        s = pygame.Surface((self.size,self.size))
        point_size = 5
        
        pygame.draw.rect(s,(0,0,0),(0,0,self.size,self.size),width=0)
        pygame.draw.rect(s,(255,255,255),(0,0,self.size,self.size),width=2)


        scale_ratio = self.size / self.fov

        point1 = Vector2(self.distance1,0).rotate(self.angle1) * scale_ratio + (self.size/2,self.size/2)
        point2 = Vector2(self.distance2,0).rotate(self.angle2) * scale_ratio + (self.size/2,self.size/2)

        pygame.draw.line(s,(255,255,255),(self.size/2,self.size/2),point1)
        pygame.draw.line(s,(255,255,255),(self.size/2,self.size/2),point2)


        pygame.draw.rect(s,(0,255,0),(self.size/2-point_size/2,self.size/2-point_size/2,point_size,point_size))
        pygame.draw.rect(s,(255,0,0),(point1.x-point_size/2,point1.y-point_size/2,point_size,point_size))
        pygame.draw.rect(s,(0,0,255),(point2.x-point_size/2,point2.y-point_size/2,point_size,point_size))


        source.blit(s,(self.x,self.y))


class GpsMarkIcon:

    def __init__(self,x,y,size,color):
        self.x,self.y = x,y
        self.size = size
        self.color = color
    def render(self,source):
        pygame.draw.rect(source,self.color,(self.x,self.y,self.size,self.size))
        
