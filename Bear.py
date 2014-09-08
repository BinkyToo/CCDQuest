import images
import random

class Bear:
    '''follows you around when in range'''
    def __init__(self, position):
        '''setup bear in given position'''
        self.position = list(position)
        self.direction = -1 # Left

    def huntplayer(self, playerpos, cellmap):
        '''move towards the player'''
        if random.random() > 0.7:
            return False
        def mindist(a, b, size):
            '''distance between two values accounting for world wrapping'''
            return min((b-a)%size,(a-b)%size)
        if (mindist(playerpos[0], self.position[0], cellmap.size[0]) +
            mindist(playerpos[1], self.position[1], cellmap.size[1])) > 15:
            return False
        def mapcoord(d_coord):
            return ((self.position[0] + d_coord[0] - 32) % cellmap.size[0],
                    (self.position[1] + d_coord[1] - 32) % cellmap.size[1])
        def istarget(d_coord):
            return (mapcoord(d_coord)[0] == playerpos[0] and
                    mapcoord(d_coord)[1] == playerpos[1])

        foundtarget = False
        dijkstramap = [[(512, (32, 32)) for x in xrange(64)] for x in xrange(64)]
        import heapq
        openlist = []
        heapq.heappush(openlist, (0, (32, 32)))
        curp = False
        while openlist:
            curn = heapq.heappop(openlist)
            curd = curn[0]
            curp = curn[1]
            if istarget(curp):
                foundtarget = True
                break
            for nbrpos in [(curp[0]-1, curp[1]), (curp[0], curp[1]-1), (curp[0]+1, curp[1]), (curp[0], curp[1]+1)]:
                if nbrpos[0] < 0 or nbrpos[1] < 0 or nbrpos[0] >= 64 or nbrpos[1] >= 64:
                    continue
                if dijkstramap[nbrpos[0]][nbrpos[1]][0] != 512 or cellmap[mapcoord(nbrpos)].solid:
                    continue
                dijkstramap[nbrpos[0]][nbrpos[1]] = (curd+1, curp)
                heapq.heappush(openlist, (curd+1, nbrpos))
        if not foundtarget:
            return False
        while dijkstramap[curp[0]][curp[1]][1] != (32, 32):
            curp = dijkstramap[curp[0]][curp[1]][1]
        self.position[0] = (self.position[0]+curp[0]-32)%cellmap.size[0]
        self.direction = curp[0]-32 if abs(curp[0]-32) else self.direction
        self.position[1] = (self.position[1]+curp[1]-32)%cellmap.size[1]
        return True
    
    def sprite(self):
        return images.BearRight if self.direction > 0 else images.BearLeft
