import random
import images
import coords
import config
import MGO

def mindist(a, b, size):
    """Distance between two values accounting for world wrapping"""
    return min((b-a)%size,(a-b)%size)

class Bear(MGO.GEMGO):
    """Harmless animal that follows the player"""
    PER_TILE = 1/config.get('fauna', 'tiles_per_bear', float, 2500)

    def __init__(self, position, cellmap):
        """Create bear at position"""
        super(Bear, self).__init__(position, cellmap)
        self.direction = -1 # Left
        self.speed = 0.7    # Chance of moving per turn, max 1, min 0
        self.pfmapsize = 32
        self.detectionrange = 18
        self.hunting = False

    def directiontoplayer(self, playerpos):
        """Find the best direction to move towards the player"""
        if (mindist(playerpos[0], self.position[0], self.cellmap.size[0]) > self.pfmapsize or
            mindist(playerpos[1], self.position[1], self.cellmap.size[1]) > self.pfmapsize):
            # Player is outside pathfinder area
            return False

        def mapcoord(pfcoord):
            """Get map coordinate from pathfinder one"""
            return coords.modsum(self.position, pfcoord, (-self.pfmapsize,)*2, self.cellmap.size)

        foundtarget = False
        dijkstramap = [[[0, (self.pfmapsize,)*2, False] for x in xrange(2*self.pfmapsize)] for x in xrange(2*self.pfmapsize)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (self.pfmapsize,)*2))
        curpos = None
        while openlist:
            curnode = heapq.heappop(openlist)
            curdist = curnode[0]
            curpos = curnode[1]
            if mapcoord(curpos) == tuple(playerpos):
                foundtarget = True
                break
            if dijkstramap[curpos[0]][curpos[1]][2] == True:
                continue
            else:
                dijkstramap[curpos[0]][curpos[1]][2] = True
            for nbrpos in coords.neighbours(curpos):
                if (nbrpos[0] < 0 or nbrpos[1] < 0 or
                    nbrpos[0] >= 2*self.pfmapsize or nbrpos[1] >= 2*self.pfmapsize or
                    nbrpos == (self.pfmapsize, self.pfmapsize)):
                    continue
                newdist = curdist+self.cellmap[mapcoord(nbrpos)]['difficulty']
                if ((dijkstramap[nbrpos[0]][nbrpos[1]][0] <= newdist and dijkstramap[nbrpos[0]][nbrpos[1]][0] != 0) or
                    self.cellmap[mapcoord(nbrpos)]['solid']):
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = [newdist, curpos, False]
                heapq.heappush(openlist, (newdist, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curpos[0]][curpos[1]][1] != (self.pfmapsize, self.pfmapsize):
            curpos = dijkstramap[curpos[0]][curpos[1]][1]
        return coords.sum(curpos, (-self.pfmapsize,)*2)

    def update(self, player):
        playerpos = player.position
        def chaseplayer():
            """Decide whether to chase the player"""
            if (mindist(playerpos[0], self.position[0], self.cellmap.size[0])**2 +
                mindist(playerpos[1], self.position[1], self.cellmap.size[1])**2) > self.detectionrange**2:
                # Can't see/smell/hear (?) player
                return False
            if random.random() > self.speed:
                # Bored?
                return False
            return True

        def randommove():
            """Move in random direction"""
            move = [0, random.randint(-1,1)]
            random.shuffle(move)
            return move

        washunting = self.hunting
        self.hunting = chaseplayer()
        if self.hunting:
            # Move in direction of player, or randomly if no path found.
            poschange = self.directiontoplayer(playerpos) or randommove()
            if washunting:
                self._suggestmessage("You are being chased by a bear", 1)
            else:
                self._suggestmessage("A bear starts chasing you", 2)
        else:
            # Move randomly.
            poschange = randommove()
            if washunting:
                self._suggestmessage("The bear has lost interest in you", 1)

        self.direction = poschange[0] if abs(poschange[0]) else self.direction
        newpos = coords.modsum(self.position, poschange, self.cellmap.size)

        if not self.cellmap[newpos]['solid']:
            self.position = newpos
        if self.position == playerpos:
            player.scattercoins(4, random.randint(4,8))
            self._suggestmessage("The bear rips a hole in your bag!", 6)

    def sprite(self, player):
        if self.position in player.visibletiles:
            return (images.BearRight if self.direction > 0 else images.BearLeft), self._pixelpos((2,2)), 1
        else:
            return None
