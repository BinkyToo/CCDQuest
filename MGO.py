import random

class MGO(object):
    def __init__(self):
        self.message = (None, 0)

    def _suggestmessage(self, string, priority):
        if priority > self.message[1]:
            self.message = [string, priority]

    def mdnotify(self):
        self.message = [None, 0]

class GEMGO(MGO):
    PER_TILE = 1/1000
    def __init__(self, position, cellmap):
        super(GEMGO, self).__init__()
        self.position = list(position)
        self.cellmap = cellmap

    @classmethod
    def place(cls, cellmap):
        '''Create set of objects with random positions'''
        created = []
        for i in xrange(cellmap.size[0]*cellmap.size[1]*cls.PER_TILE):
            attempt = (random.randint(0, cellmap.size[0]-1),
                       random.randint(0, cellmap.size[1]-1))
            created.append(cls(attempt))
        return created

    def update(self, playerpos, cellmap):
        pass


    def sprite(self):
        pass
