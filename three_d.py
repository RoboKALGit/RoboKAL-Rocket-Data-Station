

import pygame
from pygame.math import Vector3

def project(vector):
    x = vector.x
    y = -vector.y
    return pygame.math.Vector3(x, y, vector.z)


def rotate_vertices(vertices, angle, axis):
    return [v.rotate(angle, axis) for v in vertices]
def scale_vertices(vertices, s):
    return [pygame.math.Vector3(v[0]*s[0], v[1]*s[1], v[2]*s[2]) for v in vertices]
def translate_vertices(vertices, t):
    return [v + pygame.math.Vector3(t) for v in vertices]
def project_vertices(vertices):
    return [project(v) for v in vertices]


class AxisDisplay:

    def __init__(self,pos,scale,value):
        self.x, self.y = pos
        self.scale = scale

        self.vertices = [
            (1,0,0), (-1,0,0),
            (0,1,0), (0,-1,0),
            (0,0,1), (0,0,-1),
        ]

        self.vertices = [Vector3(i) for i in self.vertices]

        self.transformed_vertices = self.vertices

        self.value = value

    def render(self,source):
        
        self.transform(*self.value())

        pygame.draw.line(source, (255,0,0), (
            self.transformed_vertices[0].x + self.x,
            self.transformed_vertices[0].y + self.y,
            
        )
        , (
            self.transformed_vertices[1].x + self.x,
            self.transformed_vertices[1].y + self.y,
        ), width=4)

        pygame.draw.line(source, (0,255,0), (
            self.transformed_vertices[2].x + self.x,
            self.transformed_vertices[2].y+ self.y,
            
        )
        , (
            self.transformed_vertices[3].x + self.x,
            self.transformed_vertices[3].y + self.y,
        ), width=4)

        pygame.draw.line(source, (0,0,255), (
            self.transformed_vertices[4].x + self.x,
            self.transformed_vertices[4].y + self.y,
            
        )
        , (
            self.transformed_vertices[5].x + self.x,
            self.transformed_vertices[5].y +self.y,
        ), width=4)

    def transform(self, x,y,z):
        v = rotate_vertices(rotate_vertices(rotate_vertices(self.vertices, x, (1,0,0)),y,(0,1,0)), z, (0,0,1))
        v = scale_vertices(v, (self.scale,self.scale,self.scale))
        self.transformed_vertices = project_vertices(v)



