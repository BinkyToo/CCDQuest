import pygame
import images
import TextBox
import collectables
from colors import *

class ScoreWidget:
    '''Widget to show a score and assosciated image'''
    def __init__(self, image, window, total=None):
        self.image = image
        self.window = window
        self.prevarea = None
        self.total = total
    
    def draw(self, area, quantity):
        '''Draw the score widget'''
        area = pygame.Rect(area)
        self.window.blit(self.image, area.move(5,5))
        string = str(quantity)
        if self.total:
            string += " / " + str(self.total)
        TextBox.Print(self.window, False,
                        area.left, area.top + 65, area.width,
                        None, BLACK, 'Arial', 20,
                        string,
                        True, [False, area.height])
        pygame.draw.rect(self.window, BLACK, area, 2)

class MinimapWidget:
    '''Widget to display a small map of the whole world'''
    def __init__(self, world, window):
        self.world = world
        self.window = window

    def draw(self, area, scrollpos):
        '''Draw the minimap'''
        area = pygame.Rect(area)
        #FIXME Stretches the map if aspect ratios don't match.
        miniworld = pygame.transform.scale(self.world.surface, (area.width, area.height))
        old_clip = self.window.get_clip()
        self.window.set_clip(area)
        self.window.blit(miniworld, area)
        miniworldScale = float(area.width)/(self.world.cellmap.size[0]*images.BLOCKSIZE)
        for tx in [scrollpos[0]-self.world.surface.get_width(), scrollpos[0], scrollpos[0]+self.world.surface.get_width()]:
            for ty in [scrollpos[1]-self.world.surface.get_height(), scrollpos[1], scrollpos[1]+self.world.surface.get_height()]:
                pygame.draw.rect(self.window,
                    self.world.player.color,
                    (area.left-(tx*miniworldScale), # Top x corner of minimap, plus scroll offset
                    area.top-(ty*miniworldScale), # Top y ''
                    #FIXME should be viewport size, not window size!
                    1+ self.window.get_width()*miniworldScale,
                    1+ self.window.get_height()*miniworldScale),
                    1)
        self.window.set_clip(old_clip)

class HUD:
    def __init__(self, world, window):
        self.window = window
        self.world = world
        self.coinwidget = ScoreWidget(images.HudCoin, window, world.cellmap.origcoins)
        self.chocwidget = ScoreWidget(images.HudChoc, window)
        self.dynamitewidget = ScoreWidget(images.HudDynamite, window)
        self.minimapwidget = MinimapWidget(world, window)

    def draw(self, area, scrollpos):
        '''Draw the heads-up display, with current information'''
        area = pygame.Rect(area)
        pygame.draw.rect(self.window, WHITE, area)
        self.coinwidget.draw((area.left+10, area.top, 90, 90), self.world.player.score[collectables.COIN])
        self.chocwidget.draw((area.left+10, area.top+90, 90, 90), self.world.player.score[collectables.CHOCOLATE])
        self.dynamitewidget.draw((area.left+10, area.top+180, 90, 90), self.world.player.score[collectables.DYNAMITE])
        self.minimapwidget.draw((area.left+10, area.top+270, 90, 90), scrollpos)
    
    def endsplash(self, reason):
        '''Display a splash message across the entire window'''
        def splash(message):
            TextBox.Print(self.window, False,
                          0, 0, self.window.get_width(),
                          BLACK, WHITE, 'Arial', 40,
                          message,
                          True, [True, self.window.get_height()])
        if reason == collectables.CHOCOLATE:
            splash("You ran out of chocolate!")
        elif reason == collectables.COIN:
            splash("You found all the coins!")
        else:
            splash("What happened here?")
