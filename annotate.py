import os

from language import *

FACTOR = 2

import pygame
from pygame.locals import *
screen = pygame.display.set_mode((256*FACTOR,256*FACTOR))


from utilities import *
from fastRender import fastRender

import sys

def mouse_position():
    x,y = pygame.mouse.get_pos()
    x = x/FACTOR
    y = y/FACTOR
    y = 256 - y
    x = int(round(x/16.0,0))
    y = int(round(y/16.0,0))
    return x,y

def drawTransparent(a):
    a = np.swapaxes(a,0,1)
    a = 255*a
    a[a > 255] = 255
    a = a.astype(int)
    a = np.stack([a,a,a],axis =  -1)
    s = pygame.surfarray.make_surface(a)
    s = pygame.transform.scale(s,(256*FACTOR,256*FACTOR))
    screen.blit(s,(0,0))

def annotate(f):
    target = loadImage(f)

    program = []

    rectangle = None
    line = None
    done = False

    lastLine = None
    lastRectangle = None

    output = fastRender(Sequence(program))

    while True:
        modified = False
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN     # key down or up?
            if down:
                print event.key
                if event.key == K_RETURN: done = True
                if event.key == 117: #}u
                    program = program[:-1]
                    modified = True
                if event.key == 99: # c
                    modified = True
                    x,y = mouse_position()
                    print "Circle@",x,y
                    if x in range(1,16) and y in range(1,16):
                        program.append(Circle.absolute(x,y))
                if event.key == 114:#r
                    x,y = mouse_position()
                    if x in range(1,16) and y in range(1,16):
                        if rectangle:
                            x1 = min([x,rectangle[0]])
                            x2 = max([x,rectangle[0]])
                            y1 = min([y,rectangle[1]])
                            y2 = max([y,rectangle[1]])
                            if x1 != x2 and y1 != y2:
                                program.append(Rectangle.absolute(x1,y1,x2,y2))
                            modified = True
                            rectangle = None
                        else:
                            rectangle = (x,y)
                if event.key == 108:#l
                    x,y = mouse_position()
                    if x in range(1,16) and y in range(1,16):
                        if line:
                            [(x1,y1),(x2,y2)] = sorted([(x,y),line])
                            if x1 != x2 or y1 != y2:
                                program.append(Line.absoluteNumbered(x1,y1,x2,y2))
                                line = None
                                modified = True
                        else:
                            line = (x,y)
                if event.key == 97:#a
                    x,y = mouse_position()
                    if x in range(1,16) and y in range(1,16):
                        if line:
                            if line[0] != x or line[1] != y:
                                program.append(Line.absoluteNumbered(line[0],line[1],x,y,arrow = True))
                                line = None
                                modified = True
                        else:
                            line = (x,y)
                if event.key == 100:#d
                    x,y = mouse_position()
                    if x in range(1,16) and y in range(1,16):
                        if line:
                            [(x1,y1),(x2,y2)] = sorted([(x,y),line])
                            if x1 != x2 or y1 != y2:
                                program.append(Line.absoluteNumbered(x1,y1,x2,y2,solid = False))
                                line = None
                                modified = True
                        else:
                            line = (x,y)
                if event.key == 119:#w
                    x,y = mouse_position()
                    if x in range(1,16) and y in range(1,16):
                        if line:
                            if line[0] != x or line[1] != y:
                                program.append(Line.absoluteNumbered(line[0],line[1],x,y,solid = False,arrow = True))
                                line = None
                                modified = True
                        else:
                            line = (x,y)
        if modified:
            output = fastRender(Sequence(program))
            print "Current program:"
            print Sequence(program)
            print

        if done: break

        if line != None and lastLine == None:
            print "LINE: ",line
        lastLine = line
        if rectangle != None and lastRectangle == None:
            print "RECTANGLE:",rectangle
        lastRectangle = rectangle
        

        drawTransparent((output + target)/2.0)

        pygame.display.flip()
    print "groundTruth['%s'] = %s"%(f, set(map(str,program)))

p = sys.argv[1]
if p.endswith('png'):
    annotate(p)
else:
    for j in range(100):
        annotate(p + '/expert-%d.png'%j)
