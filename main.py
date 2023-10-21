import pygame
import os
import threading
import time

from base_class import BaseClass
from gui import UI, Label, DynamicImage, Line
from three_d import AxisDisplay
from gps import GpsDisplay, GpsMarkIcon
from graph import Graph
from missions import MissionManager

from serial_reader import Serial
from hyi_sender import Sender


DEBUG = True

pygame.init()

window = pygame.display.set_mode((1920,1080))


pygame.display.set_caption("RoboKAL Data Station")

pygame.display.set_icon(pygame.image.load("assets\\icon.png"))

background = pygame.transform.rotate(pygame.image.load("assets\\background.jpg"),90)

rocket_firing = pygame.transform.smoothscale(pygame.image.load("assets\\rocket_firing.png"),(49,187))
rocket_free = pygame.transform.smoothscale(pygame.image.load("assets\\rocket_free.png"),(49,187))

timeline_images = [pygame.transform.scale(pygame.image.load("assets\\timeline\\"+i),(960,540)) for i in os.listdir("assets\\timeline") if os.path.splitext(i)[1] == ".png"]

default_font = pygame.font.SysFont("Arial",34) #pygame.font.Font("assets\\bankgothic-regular.ttf",30)
minimal_font = pygame.font.SysFont("Arial",9)

BLACK = (0,0,0)
WHITE = (255,255,255)

WINDOW_HEIGHT_RATIO = (window.get_height()/1800)
APOGEE = 1650


base = BaseClass()

mission_manager = MissionManager()


gps_display = GpsDisplay((1600,452),250,(0,0))


altitude_graph = Graph((20,162),10,"Yükseklik (m)")

ui = UI(
    window,
    Label(20,20,"Yükseklik: {}m",default_font,WHITE,placeholders=(lambda: base.altitude,)),
    Label(20,74,"Sıcaklık: {}°C",default_font,WHITE,placeholders=(lambda: base.temperature,)),
    Label(20,452,"AÇISAL DEĞERLER",default_font,WHITE),

    Label(20,506,"X: {}°",default_font,WHITE,placeholders=(lambda: base.angle_x,)), 
    Label(20,560,"Y: {}°",default_font,WHITE,placeholders=(lambda: base.angle_y,)),
    Label(20,614,"Z: {}°",default_font,WHITE,placeholders=(lambda: base.angle_z,)),

    AxisDisplay((150,830),125,value=lambda: (i,i,i)),

    Label(1600,20,"Roket GPS Verisi:",default_font,WHITE),
    Label(1600,74,"Enlem: {}",default_font,WHITE,placeholders=(lambda: base.rocket_lat,)),
    Label(1600,128,"Boylam: {}",default_font,WHITE,placeholders=(lambda: base.rocket_lng,)),

    Label(1600,236,"Yük GPS Verisi:",default_font,WHITE),
    Label(1600,290,"Enlem: {}",default_font,WHITE,placeholders=(lambda: base.load_lat,)),
    Label(1600,344,"Boylam: {}",default_font,WHITE,placeholders=(lambda: base.load_lng,)),

    gps_display,

    GpsMarkIcon(1650,707,9,(0,255,0)),
    GpsMarkIcon(1700,707,9,(255,0,0)),
    GpsMarkIcon(1740,707,9,(0,0,255)),
    Label(1645,707,"      Yer İst.      Roket      Yük",minimal_font,WHITE),

    GpsMarkIcon(1600, 756, 34, (255,0,0)),
    Label(1650,756,"{}m ( {}° )",default_font,WHITE,placeholders=(lambda: int(gps_display.distance1*1000), lambda: int(gps_display.angle1 if gps_display.angle1 >= 0 else 360 + gps_display.angle1))),
    GpsMarkIcon(1600, 810, 34, (0,0,255)),
    Label(1650,810,"{}m ( {}° )",default_font,WHITE,placeholders=(lambda: int(gps_display.distance2*1000), lambda: int(gps_display.angle2 if gps_display.angle2 >= 0 else 360 + gps_display.angle2))),

    DynamicImage(480,540,timeline_images,lambda: mission_manager.mission_state),

    altitude_graph,

    Line((960-400,1080-APOGEE*WINDOW_HEIGHT_RATIO),(960+400,1080-APOGEE*WINDOW_HEIGHT_RATIO),WHITE,width=2),
    Label(960-400,1080-APOGEE*WINDOW_HEIGHT_RATIO-36,f"Apogee: {APOGEE}m",default_font,WHITE)
)


def serial_receiver():
    global base

    source_serial = Serial("COM4",9600)

    while True:
        raw_data = source_serial.read()
        
        match raw_data[0]:
            case 0:
                base.altitude = raw_data[0]
                base.temperature = raw_data[1]
                base.rocket_gps_altitude = raw_data[2]
                base.rocket_lat = raw_data[3]
                base.rocket_lng = raw_data[4]
                base.gyro_x = raw_data[5]
                base.gyro_y = raw_data[6]
                base.gyro_z = raw_data[7]
                base.accel_x = raw_data[8]
                base.accel_y = raw_data[9]
                base.accel_z = raw_data[10]
                base.angle_x = raw_data[11]
                base.angle_y = raw_data[12]
                base.angle_z = raw_data[13]
                base.state = raw_data[14]

                altitude_graph.plot(base.altitude)

            case 1:
                base.load_gps_altitude = raw_data[2]
                base.load_lat = raw_data[3]
                base.load_lng = raw_data[4]

        mission_manager.complete_startup()
        mission_manager.complete_transmission((base.rocket_gps_altitude,base.rocket_lat,base.rocket_lng),(base.load_gps_altitude,base.load_lat,base.load_lng))
        mission_manager.complete_liftoff(base.altitude)
        mission_manager.complete_deploy(base.state)
        mission_manager.complete_freefall(base.altitude)


def serial_sender():
    target_serial = Sender("COM5",9600)
    while True:
        target_serial.send(base.__dict__)
        time.sleep(1/10)
        

if not DEBUG:
    threading.Thread(target=serial_receiver,daemon=True).start()
    threading.Thread(target=serial_sender,daemon=True).start()


i = 0


clock = pygame.time.Clock()

while True:

    clock.tick(60)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            quit()

    #window.fill(BLACK)
    window.blit(background, (0,0))

    gps_display.set_coordinates((base.rocket_lat,base.rocket_lng),(base.load_lat,base.load_lng))

    ui.render()

    window.blit(rocket_firing,(window.get_width()//2-rocket_firing.get_width()//2, window.get_height() + -base.altitude * WINDOW_HEIGHT_RATIO - rocket_firing.get_height()))

    pygame.display.flip()

    i += 1


    
    

