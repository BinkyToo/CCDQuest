import images
import MGO

class Sign(MGO.GEMGO):
    """Sign that displays message when walked over"""
    def __init__(self, string, position, cellmap):
        """Create new sign in position"""
        super(Sign, self).__init__(position, cellmap)
        self.string = string
        self.visible = False

    @classmethod
    def place(cls, cellmap):
        created = []
        for signdef in cellmap.signdefs:
            created.append(cls(signdef[1], signdef[0], cellmap))
        return created

    def update(self, player):
        """Display message if becoming visible or trodden on"""
        if self.position == player.position:
            self._suggestmessage("The sign reads: " + self.string, 50)

        if self.position in player.visibletiles:
            if not self.visible:
                self._suggestmessage("You see a sign in the distance", 1)
            self.visible = True
        else:
            self.visible = False

    def sprite(self, player):
        if self.cellmap[self.position]['explored']:
            return images.Sign, self._pixelpos(), -1
        else:
            return None
