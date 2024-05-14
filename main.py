#import libraries to be used
import pygame as py
from pygame import Vector2 as Vec2
import random, sys

#import other files
from colors import *
from boid import *
from helpfunctions import *

py.init() # initialize pygame
screen_width, screen_height = 1600, 900 # define screen width and height
py.display.set_caption("Boids") # set caption for pygame window

running = True # game running bool
debug_boids = False # determines whether debug settings are used

window_flags = py.DOUBLEBUF # | py.FULLSCREEN
window = py.display.set_mode((screen_width, screen_height), window_flags, 8) # pygame window
clock = py.time.Clock() # pygame clock
fps = 60 # fps, frames per second

font_arial30 = py.font.SysFont('Arial', 30) # font to be used, along with font size

blue_arrow_img = py.image.load('blue_arrow.png').convert_alpha() # boid image
add_boid_text = font_arial30.render("T - Add Boid", True, WHITE) # constant text doesnt need to be re-rendered every frame
toggle_debug_text = font_arial30.render("N - Toggle Debug Rays", True, WHITE) # constant text doesnt need to be re-rendered every frame
boid_count = 0 # boid counter

flock_params = FlockParams(separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1) # flock parameters

sections = { # sections dictionary for optimization
    0: { 0: {}, 1: {}, 2: {} },
    1: { 0: {}, 1: {}, 2: {} },
    2: { 0: {}, 1: {}, 2: {} },
    3: { 0: {}, 1: {}, 2: {} }
}

for i in range(100):
    pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height)) # randomize position
    vel = Vec2(random.uniform(-1,1), random.uniform(-1,1)) # randomize velocity
    accel = Vec2(1,1) # set acceleration
    
    boid = Boid(pos, vel, accel, blue_arrow_img) # create boid
    sections[boid.section[0]][boid.section[1]][(boid.id)] = boid # add boid to section
    boid_count +=1 # increase boid count

while running: # main loop
    clock.tick(fps) # tick fps
    fps_text = font_arial30.render("FPS: " + str(round(clock.get_fps())), True, WHITE) # render fps text
    boid_count_text = font_arial30.render("BOIDS: " + str(boid_count), True, WHITE) # render num boid text

    for e in py.event.get():

        if e.type == py.QUIT: # quit game
            running = False # no longer running
            sys.exit() # exit application
        
        if e.type == py.KEYDOWN: # key pressed down
            key = e.key # current key

            if key == py.K_t: # key is t
                pos = Vec2(random.randint(0,screen_width), random.randint(0,screen_height)) # randomize position
                vel = Vec2(random.uniform(-1,1), random.uniform(-1,1)) # randomize velocity
                accel = Vec2(1,1) # set acceleration
                
                boid = Boid(pos, vel, accel, blue_arrow_img) # create boid
                sections[boid.section[0]][boid.section[1]][(boid.id)] = boid # add boid to section
                boid_count +=1 # increase boid count

            if key == py.K_n: # key is n
                debug_boids = not debug_boids # change debug setting

    window.fill(DARKGRAY) # fill window with color
    
    for x in sections.keys(): # loop through section rows
        for y in sections[x].keys(): # loop through section columns
            for boid in sections[x][y].values(): # loop through boids in section
                boid.Flock(sections[x][y], flock_params) # Add forces to boid
                boid.Update() # Update boid
                sections = boid.UpdateSections(sections) # Update boid sections
                if debug_boids: # Check if debugging
                    direction_ray = Ray(boid.pos, boid.vel, 15) # Create ray
                    direction_ray.DebugDraw(window) # Draw ray
                boid.Draw(window) # Draw boid

    # Draw text items on screen
    window.blit(fps_text, (100, 50))
    window.blit(boid_count_text, (100, 100))
    window.blit(add_boid_text, (100, 150))
    window.blit(toggle_debug_text, (100,200))
    # Update screen
    py.display.update() 

py.quit() # Quit pygame when loop ends