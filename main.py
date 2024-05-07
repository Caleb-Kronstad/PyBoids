#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import numpy as np
import random, sys, math

#import other files
from colors import *
from boid import *
from helpfunctions import *

py.init() # initialize pygame
screen_width, screen_height = 1600, 900 # define screen width and height
py.display.set_caption("Boids") # set caption for pygame window

running = True # game running bool
debug_boids = True # determines whether debug settings are used

window_flags = py.DOUBLEBUF # | py.FULLSCREEN
window = py.display.set_mode((screen_width, screen_height), window_flags, 8)
clock = py.time.Clock()
fps = 60

font_arial30 = py.font.SysFont('Arial', 30)
time_scale = 1

blue_arrow_img = py.image.load('blue_arrow.png').convert_alpha()
add_boid_text = font_arial30.render("Press 'T' to add a boid", True, WHITE)
boid_count = 0

flock_params = FlockParams(50, 100, 200, 1, 1, 1)

sections = {
    0: { 0: {}, 1: {}, 2: {} },
    1: { 0: {}, 1: {}, 2: {} },
    2: { 0: {}, 1: {}, 2: {} },
    3: { 0: {}, 1: {}, 2: {} }
}

for i in range(100):
    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
    accel = Vec2(1,1)
    
    boid = Boid(pos, vel, accel, blue_arrow_img)
    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid
    boid_count += 1

    t_down = False

while running:
    clock.tick(fps)
    fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, WHITE)
    boid_count_text = font_arial30.render("BOIDS: " + str(boid_count), True, WHITE)

    for e in py.event.get():
        if e.type == py.QUIT: 
            running = False
            sys.exit()
        
        if e.type == py.KEYDOWN:
            if e.key == py.K_t and t_down == False:
                t_down = True
                pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height))
                vel = Vec2(random.uniform(-1,1), random.uniform(-1,1))
                accel = Vec2(1,1)
                
                boid = Boid(pos, vel, accel, blue_arrow_img)
                sections[boid.section[0]][boid.section[1]][(boid.id)] = boid
                boid_count +=1 
        
        if e.type == py.KEYUP:
            if e.key == py.K_t:
                t_down = False

    window.fill(DARKGRAY)
    
    for x in sections.keys():
        for y in sections[x].keys():
            for boid in sections[x][y].values():
                #Add forces to boid
                boid.Flock(sections[x][y], flock_params = flock_params)
                #Update
                boid.Update(1)
                sections = boid.UpdateSections(sections)
                #Draw
                if debug_boids:
                    direction_ray = Ray(boid.pos, boid.vel, 15)
                    direction_ray.DebugDraw(window)
                boid_rect = boid.Draw(window)

    # Draw text
    window.blit(fps_text, (100, 50))
    window.blit(boid_count_text, (100, 100))
    window.blit(add_boid_text, (100, 150))
    # Update screen
    py.display.update() 

py.quit()