import pygame
import random
import collectables
import images
from Bear import Bear
from Dragon import Dragon
from Pixie import Pixie
from Sign import Sign
from Map import Map
from Player import Player
from colors import *
import time

TILESIZE = images.TILESIZE

class World:
    def __init__(self, mapdict):
        self.cellmap = Map(mapdict)
        self.surface = pygame.Surface((self.cellmap.size[0]*TILESIZE, self.cellmap.size[1]*TILESIZE))
        self.surface.fill(BLACK)

        self.gemgos = []
        for gemgo in Player, Bear, Dragon, Sign, Pixie:
            self.gemgos += gemgo.place(self.cellmap)
        self.player = filter(lambda x: isinstance(x, Player), self.gemgos)[0]

    def rendervisibletiles(self, extrasprites=[]):
        a = time.clock()
        self.player.updatevisible()
        for tile in self.player.visibletiles:
            cell = self.cellmap[tile]
            cell['explored'] = True
        if not self.cellmap[self.player.position]['transparent']:
            self.player.visibletiles.remove(tuple(self.player.position))
        sprites = extrasprites

        visibleranges = ([],[])
        for axis in [0, 1]:
            if 2*self.player.visibility + 1 >= self.cellmap.size[axis]:
                visibleranges[axis].append((0, self.cellmap.size[axis]))
            else:
                rmin = (self.player.position[axis] - self.player.visibility) % self.cellmap.size[axis]
                rmax = (self.player.position[axis] + self.player.visibility) % self.cellmap.size[axis]
                if rmin < rmax:
                    visibleranges[axis].append((rmin, rmax))
                else:
                    visibleranges[axis].append((rmin, self.cellmap.size[axis]))
                    visibleranges[axis].append((0, rmax))

        for rx in visibleranges[0]:
            for ry in visibleranges[1]:
                self.surface.set_clip(
                    rx[0]*TILESIZE, ry[0]*TILESIZE,
                    (rx[1]-rx[0])*TILESIZE, (ry[1]-ry[0])*TILESIZE)
                regionsprites = sprites
                for ix in range(rx[0]-1, rx[1]+1):
                    for iy in range(ry[0]-1, ry[1]+1):
                        regionsprites += self.cellmap.sprites((ix, iy))
                        if (ix%self.cellmap.size[0], iy%self.cellmap.size[1]) not in self.player.visibletiles:
                            sprites.append((images.NonVisible, (ix*TILESIZE, iy*TILESIZE), 100))
                regionsprites.sort(key=lambda x: x[2])
                for sprite in regionsprites:
                    self.surface.blit(sprite[0], sprite[1])
        print time.clock() - a

    def moveplayer(self, arg):
        '''Move the player by (x, y), move other fauna, update world surface around player'''
        self.cellmap.update()
        self.player.action(arg)

        gemgosprites = []
        for gemgo in self.gemgos:
            gemgo.update(self.player)
            sprite = gemgo.sprite(self.player)
            if sprite is not None:
                gemgosprites.append(sprite)

        self.rendervisibletiles(gemgosprites)

        if tuple(self.player.position) in self.cellmap.burningtiles:
            self.player.score[collectables.CHOCOLATE] -= Map.CELLBURNINGCOST
