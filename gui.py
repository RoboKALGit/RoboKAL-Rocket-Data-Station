import pygame

class Label:

    def __init__(self,x,y,text,font,color,align="left",placeholders=()):
        self.x, self.y = x,y
        self.text: str = text
        self.font: pygame.font.Font = font
        self.color: tuple[int,int,int] = color
        self.align: str = align
        self.placeholders = placeholders
    def render(self,source):
        surface = self.font.render(self.text.format(*[i() for i in self.placeholders]),True,self.color)

        rect = surface.get_rect()

        match self.align:
            case "left":
                rect.left = self.x
            case "right":
                rect.right = self.x

        rect.top = self.y

        source.blit(surface,rect)


class DynamicImage:

    def __init__(self,x,y,frames,variable):
        self.x, self.y = x,y
        self.frames = frames
        self.variable = variable
    def render(self,source):
        source.blit(self.frames[self.variable()],(self.x,self.y))

class Line:

    def __init__(self,p1,p2,color,width=1):
        self.p1, self.p2 = p1, p2
        self.color = color
        self.width = width
    
    def render(self,source):
        pygame.draw.line(source,self.color,self.p1,self.p2,width=self.width)


class UI:
    
    def __init__(self,main_surface,*components):
        self.main_surface = main_surface
        self.components = components
    
    def render(self):
        for i in self.components:
            i.render(self.main_surface)