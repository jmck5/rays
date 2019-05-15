##This is the Ray Casting program from Daniel Shiffman's Coding Train
## https://www.youtube.com/watch?v=TOEi6T2mtHo
## The original is in p5.js, I have tried to port it to pygame

import pygame, sys
from pygame.locals import *
import random
import math 

## I think this needs to be global so classes can access it?
global screen


## Calculate the distance between two points
def dist(p1,p2):   
    x1,y1=p1
    x2,y2=p2
    d= ((x2-x1)**2+(y2-y1)**2)**(1/2)
    return d

## Takes an angle in degrees and returns cartesian coordinates    
def twodvecFromAngle(angle):
    x= math.sin(math.radians(angle))
    y=math.cos(math.radians(angle))
    return (x,y)


class Ray:
    ## Initialise the ray instance with a source position and a direction
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = twodvecFromAngle(angle)

    ## 
    ##Incomplete but seems to work okay
    def lookAt(self,x,y):
        self.dir.x = x - self.pos.x
        self.dir.y = y- self.pos.y
        ##self.dir.normalise() ## need to somehow normalise this
        
    ## This algorithm is by Shiffman using a formula from Wikipedia line-line intersection page
    ## It checks if a ray will interesect with a wall
    ## but to be honest I don't completely understand it yet
    ## If the ray interesects it will return the pt it interesects/hits the wall

    def cast(self,wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

        x3=self.pos[0] 
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        denominator = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        if denominator == 0:
            return
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/denominator
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/denominator

        if ((t>0.0) & (t<1.0) & (u>0.0)):
            pt = ((x1+(t*(x2-x1))),(y1+(t*(y2-y1))))
            return pt
        return

    ## This shows the direction of all rays
    ## With a radius of 10 around the source
    def show(self):
        raycolour = (0,0,200)
        ##pygame.translate(self.pos[0],self.pos[1])
        pygame.draw.line(screen, raycolour,(self.pos),(self.pos[0]+self.dir[0]*10, self.pos[1]+self.dir[1]*10),1 )
    ## We need to update the position of the source of the rays
    ## In the p5.js version the ray source and particle position are always the same
    ## But in this code I have to update them both

    def update(self,newpos):
        self.pos = newpos    
        
        
## This class defines 'walls' for the light to hit        
class Boundary:
    def __init__(self, x1,y1,x2,y2):
        self.a = (x1,y1)
        self.b = (x2,y2)

    def show(self):
        pygame.draw.line(screen, (250,0,0), (self.a[0], self.a[1]),(self.b[0],self.b[1]),2)

## Particle class.
## Rays are supposed to be cast from a particle which can be moved by the mouse
class Particle:
    def __init__(self):
        self.pos = (100,100)
        self.rays=[];
        for a in range(0,360,10):
            self.rays.append(Ray(self.pos, a))

    def look(self,walls):
        for ray in self.rays:
            closest = False
            record = 99999
            for wall in walls:
                pt = ray.cast(wall) ## This will only have a value if cast returns a point ie light hits the wall
                if(pt):  ##If light hits a wall 
    
                    d = dist(self.pos, pt) ## Work out the distance
                   
                    if d<record: ##The light should hit the closest wall and go no further, so we are checking which 'hit' is closest
                        record = d
                        closest = pt
            ## If there is a closest point we draw the ray from the source to the point the ray hits
            ## i.e. here we draw only rays that hit a wall
            if(closest):
                pygame.draw.line(screen, (25,200,250), (self.pos),(closest),1)

    #Update particle position and ray source. They should really be the same, but this solves an error where they initialised in the same point but then went separate ways
    # Which led to some interesting drawings actually where the rays were cast from the particle to where they would have been cast if the particle had never moved...
    def update(self,newpos):
        self.pos = newpos
        for r in self.rays: ##interestingly in p5 it seems the constructor for rays means the ray.pos is always the particle.pos value
            r.pos = newpos  ##whereas here it seems that it is just the initial value so we have to update it here

    ## Draw the particle as a circle. then call the function to draw the rays
    def show(self):
        #
        red=(250,100,100)
        pygame.draw.circle(screen, red,self.pos,5)
        for i in range(len(self.rays)):
            self.rays[i].show()


##setupPyGame
pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.init()

##Create n walls placed randomly
n=87
walls =[]
for i in range (n):
    xa = random.randint(1,600)
    ya = random.randint(1,400)
    xb = random.randint(1,600)
    yb = random.randint(1,400)
    walls.append(Boundary(xa,ya,xb,yb))
## Create particle
p = Particle  ()



while True:
    ##Refresshes the background each time otherwise we end up with the ghost
    screen.fill((20,20,20))
    
    p.show()
    for wall in walls:
        wall.show()
    p.look(walls)
    ## Use mouse to move particle
    p.update(pygame.mouse.get_pos())
    ## Refresh the display
    pygame.display.update()
    ## Include pygame quit feature
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
