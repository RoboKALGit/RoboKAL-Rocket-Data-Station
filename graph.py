
import matplotlib.pyplot as plt
from matplotlib import use
import matplotlib.backends.backend_agg as agg
import random
import pygame

 
use("Agg")

class Graph:

    def __init__(self,pos,max_length,label) -> None:
        self.x, self.y = pos
        self.max_length = max_length
        self.label = label

        self.values = []
        self.output_surface = None

        self.plot(None)

    def plot(self,value):

        if value:
            if len(self.values) >= self.max_length:
                self.values.pop(0)
            self.values.append(value)

        fig = plt.figure(facecolor='black')

        ax = plt.axes()

        ax.set_facecolor("black")
        ax.get_xaxis().set_ticks([])
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.tick_params(axis='y', colors='white')

        plt.ylabel(self.label, fontweight='bold',color="white")

        plt.plot(self.values, color="green")

        
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        self.output_surface = pygame.transform.smoothscale(pygame.image.fromstring(raw_data, size, "RGB"),(320,240))
    
    def render(self,source):
        source.blit(self.output_surface,(self.x,self.y))









