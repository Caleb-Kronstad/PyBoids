#imports
import pygame as py
from pygame import Vector2 as Vec2
from numpy import arctan2, pi
import random, sys

from colors import *
from helpfunctions import *

class FlockParams(): # Params for flock calculations
    def __init__(this, separation_distance = 50, alignment_distance = 100, cohesion_distance = 200, separation_factor = 1, alignment_factor = 1, cohesion_factor = 1):
        this.separation_distance = separation_distance # max distance for separation calculation to take place
        this.alignment_distance = alignment_distance # max distance for aligment calculation to take place
        this.cohesion_distance = cohesion_distance # max distance for cohesion calculation to take place
        this.separation_factor = separation_factor # multiplier for separation calculation
        this.alignment_factor = alignment_factor # multiplier for alignment calculation
        this.cohesion_factor = cohesion_factor # multiplier for cohesion calculation

class Boid: # Boid class
    def __init__(this, pos, vel, accel, img, mass=1):
        this.id = random.randint(-sys.maxsize-1, sys.maxsize) # randomize id 

        this.pos = pos # position of boid
        this.accel = accel # boid acceleration
        this.mass = mass # boid mass
        
        if Normalize(vel) > 0: # check velocity greater than 0
            this.vel = vel / Normalize(vel) # normalize velocity
        else: # velocity is zero
            this.vel = Vec2(0,0) # velocity zero

        this.max_force = 0.2 # max force
        this.max_speed = 4 # max speed

        this.img = img # boid image
        this.saved_img = img # boid image saved
        this.rect = this.img.get_rect(center = this.pos) # boid rect

        this.forces = accel * mass # forces based on acceleration and mass

        this.section = FindBoidSection(this) # current section
        this.previous_section = this.section # previous section

    def Flock(this, boids, flock_params = FlockParams()): # calculate flock forces function
        alignment_force = Vec2(0,0) # alignment force vector
        cohesion_force = Vec2(0,0) # cohesion force vector
        separation_force = Vec2(0,0) # separation force vector
        alignment_neighbors = 0 # alignment neighbors
        cohesion_neighbors = 0 # cohesion neighbors
        separation_neighbors = 0 # separation neighbors

        for other in boids.values(): # loop through boids
            if other == this: continue # check that the current boid is not the one in the loop

            dist = Normalize(other.pos-this.pos) # distance between boid and other boid

            if dist < flock_params.alignment_distance: # in range for alignment
                alignment_force += other.vel # add to alignment force
                alignment_neighbors += 1 # increase alignment neighbors

            if dist < flock_params.cohesion_distance: # in range for cohesion
                cohesion_force += other.pos # add to cohesion force
                cohesion_neighbors += 1 # increase cohesion neighbors

            if dist < flock_params.separation_distance: # in range for separation
                diff = this.pos - other.pos # get difference between boid positions
                if dist == 0: # check distance is zero
                    dist = 0.000001 # set to very small so no division by zero
                diff *= 1 / dist # multiple difference by 1/difference 
                separation_force += diff # add to separation force
                separation_neighbors += 1 # increase separation neighbors
        
        if alignment_neighbors > 0: # check for alignment neighbors
            alignment_force /= alignment_neighbors # divide alignment force by number of neighbors
            alignment_force = SetMagnitude(alignment_force, this.max_speed) # set magnitude to max speed
            alignment_force -= this.vel # subtract by boid velocity
            alignment_force = LimitMagnitude(alignment_force, this.max_force) * flock_params.alignment_factor # limit magnitude to max force and multiply by alignment factor

        if cohesion_neighbors > 0: # check for cohesion neighbors
            cohesion_force /= cohesion_neighbors # divide cohesion force by number of neighbors
            cohesion_force -= this.pos # subtract by boid position
            cohesion_force = SetMagnitude(cohesion_force, this.max_speed) # set magnitude to max speed
            cohesion_force -= this.vel # subtract by boid velocity
            cohesion_force = LimitMagnitude(cohesion_force, this.max_force) * flock_params.cohesion_factor # limit magnitude to max force and multiply by cohesion factor
        
        if separation_neighbors > 0: # check for separation neighbors
            separation_force /= separation_neighbors # divide separation force by number of neighbors
            separation_force = SetMagnitude(separation_force, this.max_speed) # set magnitude to max speed
            separation_force -= this.vel # subtract by boid velocity
            separation_force = LimitMagnitude(separation_force, this.max_force) * flock_params.separation_factor # limit magnitude to max force and multiply by separation factor

        this.AddForce(cohesion_force) # add cohesion force
        this.AddForce(alignment_force) # add alignment force
        this.AddForce(separation_force) # add separation force

    def AddForce(this, force = Vec2(0,0)): # add force to boid
        this.forces += force # add force

    def UpdateSections(this, sections): # update sections based on current position
        temp_sections = sections
        if this.section != this.previous_section and this.id in temp_sections[this.previous_section[0]][this.previous_section[1]]: # check if in a different section and id is valid
            temp_sections = {x: {y: dict(sections[x][y]) for y in sections[x]} for x in sections} # copy sections
            temp_sections[this.previous_section[0]][this.previous_section[1]].pop(this.id) # remove from previous section
            temp_sections[this.section[0]][this.section[1]].update({this.id: this}) # add to new section
            this.previous_section = this.section # update previous section
        return temp_sections # return sections

    def Update(this): # update boid
        this.accel = this.forces / this.mass # calculate the acceleration based on current frame forces and boid's mass
        this.vel = LimitMagnitude(this.vel + this.accel, this.max_speed) # update velocity based on acceleration, but limit the magnitude of the vector to the max speed
        this.pos += this.vel # update position based on current velocity
        this.forces = Vec2(0,0) # reset forces for next frame

        this.img = py.transform.rotate(this.saved_img, (180/pi) * (arctan2(-this.vel.y, this.vel.x) - (90 * (pi/180)))) # rotate boid image -- due to pygame's skewed coordinate system the rotation has to be altered slightly (hence the negative y axis)

        # keep the boids on screen
        if this.pos.x > 1600:
            this.pos.x = 0
        elif this.pos.x < 0:
            this.pos.x = 1600
        if this.pos.y > 900:
            this.pos.y = 0
        elif this.pos.y < 0:
            this.pos.y = 900

        # find which section the boid is currently in for optimization (only test other boids in the same section)
        this.section = FindBoidSection(this)

    def Draw(this, window): # Draw boid on screen
        this.rect = this.img.get_rect(center = this.pos) # define rect
        draw_rect = window.blit(this.img, this.rect) # draw image
        return draw_rect # return draw rect
    