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

class Boid:
    def __init__(this, pos, vel, accel, img, mass=1):
        this.id = random.randint(-sys.maxsize-1, sys.maxsize)

        this.in_flock = False
        this.pos = pos
        this.accel = accel
        this.mass = mass

        this.cohesion_enabled = True
        this.alignment_enabled = True
        this.separation_enabled = True
        
        if Normalize(vel) > 0:
            this.vel = vel / Normalize(vel)
        else:
            this.vel = Vec2(0,0)

        this.max_force = 0.2
        this.max_speed = 4

        this.img = img
        this.saved_img = img
        this.rect = this.img.get_rect(center = this.pos)

        this.forces = accel * mass

        this.section = FindBoidSection(this)
        this.previous_section = this.section

    def Flock(this, boids, flock=None, flock_params = FlockParams()):
        alignment_force = Vec2(0,0)
        cohesion_force = Vec2(0,0)
        separation_force = Vec2(0,0)
        alignment_neighbors = 0
        cohesion_neighbors = 0
        separation_neighbors = 0

        if flock==None:
            for other in boids.values():
                if other == this: continue

                dist = Normalize(other.pos-this.pos)

                if dist < flock_params.alignment_distance:
                    alignment_force += other.vel
                    alignment_neighbors += 1

                if dist < flock_params.cohesion_distance:
                    cohesion_force += other.pos
                    if flock != None:
                        cohesion_force += flock.pos - other.pos
                    cohesion_neighbors += 1

                if dist < flock_params.separation_distance:
                    diff = this.pos - other.pos
                    if dist == 0:
                        dist = 0.000001
                    diff *= 1 / dist
                    separation_force += diff
                    separation_neighbors += 1
            
            if alignment_neighbors > 0:
                alignment_force /= alignment_neighbors
                alignment_force = SetMagnitude(alignment_force, this.max_speed)
                alignment_force -= this.vel
                alignment_force = LimitMagnitude(alignment_force, this.max_force) * flock_params.alignment_factor

            if cohesion_neighbors > 0:
                cohesion_force /= cohesion_neighbors
                cohesion_force -= this.pos
                cohesion_force = SetMagnitude(cohesion_force, this.max_speed)
                cohesion_force -= this.vel
                cohesion_force = LimitMagnitude(cohesion_force, this.max_force) * flock_params.cohesion_factor
            
            if separation_neighbors > 0:
                separation_force /= separation_neighbors
                separation_force = SetMagnitude(separation_force, this.max_speed)
                separation_force -= this.vel
                separation_force = LimitMagnitude(separation_force, this.max_force) * flock_params.separation_factor

            if cohesion_neighbors == 0 and flock != None and this.in_flock:
                cohesion_force += flock.pos - this.pos
                cohesion_force = SetMagnitude(cohesion_force, this.max_speed)
                cohesion_force -= this.vel
                cohesion_force = LimitMagnitude(cohesion_force, this.max_force) * flock_params.cohesion_factor

            if this.cohesion_enabled: this.AddForce(cohesion_force)
            if this.alignment_enabled: this.AddForce(alignment_force)
            if this.separation_enabled: this.AddForce(separation_force)
        else:
            for other in boids:
                if other == this: continue

                dist = Normalize(other.pos-this.pos)

                if dist < flock_params.alignment_distance:
                    alignment_force += other.vel
                    alignment_neighbors += 1

                if dist < flock_params.cohesion_distance:
                    cohesion_force += other.pos
                    if flock != None:
                        cohesion_force += flock.pos - other.pos
                    cohesion_neighbors += 1

                if dist < flock_params.separation_distance:
                    diff = this.pos - other.pos
                    if dist == 0:
                        dist = 0.000001
                    diff *= 1 / dist
                    separation_force += diff
                    separation_neighbors += 1
            
            if alignment_neighbors > 0:
                alignment_force /= alignment_neighbors
                alignment_force = SetMagnitude(alignment_force, this.max_speed)
                alignment_force -= this.vel
                alignment_force = LimitMagnitude(alignment_force, this.max_force) * flock_params.alignment_factor

            if cohesion_neighbors > 0:
                cohesion_force /= cohesion_neighbors
                cohesion_force -= this.pos
                cohesion_force = SetMagnitude(cohesion_force, this.max_speed)
                cohesion_force -= this.vel
                cohesion_force = LimitMagnitude(cohesion_force, this.max_force) * flock_params.cohesion_factor
            
            if separation_neighbors > 0:
                separation_force /= separation_neighbors
                separation_force = SetMagnitude(separation_force, this.max_speed)
                separation_force -= this.vel
                separation_force = LimitMagnitude(separation_force, this.max_force) * flock_params.separation_factor

            if cohesion_neighbors == 0 and flock != None and this.in_flock:
                cohesion_force += flock.pos - this.pos
                cohesion_force = SetMagnitude(cohesion_force, this.max_speed)
                cohesion_force -= this.vel
                cohesion_force = LimitMagnitude(cohesion_force, this.max_force) * flock_params.cohesion_factor

            if this.in_flock:
                if this.cohesion_enabled: this.AddForce(cohesion_force)
                if this.alignment_enabled: this.AddForce(alignment_force)
                if this.separation_enabled: this.AddForce(separation_force)

    def AddForce(this, force = Vec2(0,0)):
        this.forces += force

    def UpdateSections(this, sections):
        temp_sections = sections
        if this.section != this.previous_section and this.id in temp_sections[this.previous_section[0]][this.previous_section[1]]:
            temp_sections = {x: {y: dict(sections[x][y]) for y in sections[x]} for x in sections}
            temp_sections[this.previous_section[0]][this.previous_section[1]].pop(this.id)
            temp_sections[this.section[0]][this.section[1]].update({this.id: this})
            this.previous_section = this.section

        return temp_sections

    def Update(this, ts, flock=None):
        this.accel = this.forces / this.mass # calculate the acceleration based on current frame forces and boid's mass
        this.vel = LimitMagnitude(this.vel + this.accel * ts, this.max_speed) # update velocity based on acceleration, but limit the magnitude of the vector to the max speed
        this.pos += this.vel * ts # update position based on current velocity
        if flock != None: this.pos -= flock.vel * ts
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

    def Draw(this, window):
        this.rect = this.img.get_rect(center = this.pos)
        draw_rect = window.blit(this.img, this.rect)
        return draw_rect
    