#imports
import pygame as py
from pygame import Vector2 as Vec2
import math
from colors import *

class Ray: # used for debugging directions of boids
    def __init__(this, pos, direction, distance):
        this.pos = pos # position of ray
        this.direction = direction # direction of ray
        this.distance = distance # distance or length of ray

    def DebugDraw(this, window, color=RED, width=1): # draw ray
        py.draw.line(window, color,
                     (this.pos.x, this.pos.y), 
                     (this.direction.x * this.distance + this.pos.x, this.direction.y * this.distance + this.pos.y),
                     width)

#Some functions I created

def Normalize(vector): # using my own rather than np.linalg.norm gives a 30 fps boost alone -- crazy
    return math.sqrt(vector[0]**2 + vector[1]**2)

def LimitMagnitude(vector, limit): # limits vector magnitude (length of vector)
    magnitude = Normalize(vector) # get the magnitude of the vector
    if magnitude > limit: # check if the magnitude is greater than the limit
        normalized_vector = vector / magnitude # normalize the vector
        limited_vector = normalized_vector * limit # limit the vector
        return limited_vector # return the limited vector
    else: # magnitude is not greater than the limit
        return vector # return the original vector
    
def SetMagnitude(vector, magnitude): # sets vector magnitude (length of vector)
    if (Normalize(vector) != 0): # check not zero so we dont have divison by zero
        normalized_vector = vector / Normalize(vector) # normalize vector
    else: # is zero
        return Vec2(0,0) # return vector zero
    scaled_vector = normalized_vector * magnitude # scale vector length
    return scaled_vector # return scaled vector

def FindBoidSection(boid): # Finds section boid is currently in for performance increase
    xs = 0 # x section
    ys = 0 # y section
    
    # check x position and change x section based on position
    if boid.pos.x > 1200:
        xs = 3
    elif boid.pos.x > 800:
        xs = 2
    elif boid.pos.x > 400:
        xs = 1

    # check y position and change y section based on position
    if boid.pos.y > 600:
        ys = 2
    elif boid.pos.y > 300:
        ys = 1
    
    # return x and y sections
    return [xs,ys]