import pygame
import collectables
from colors import MAGENTA
from directions import *

'''Load and convert all in-game images'''

# Size of terrain sprites.
TILESIZE = 12

# Images with transparency use convert_alpha().

TerrainSprites = [
    [
        'wall',
        pygame.image.load("tiles/Wall.png").convert()
    ],
    [
        'glass',
        pygame.image.load("tiles/Glass.png").convert(),
    ],
    [
        'tree',
        pygame.image.load("tiles/Trees1.png").convert(),
        pygame.image.load("tiles/Trees2.png").convert(),
        pygame.image.load("tiles/Trees3.png").convert(),
        pygame.image.load("tiles/Trees4.png").convert(),
        pygame.image.load("tiles/Trees5.png").convert(),
        pygame.image.load("tiles/Trees6.png").convert(),
        pygame.image.load("tiles/Trees7.png").convert(),
        pygame.image.load("tiles/Trees8.png").convert(),
    ],
    [
        'snow',
        pygame.image.load("tiles/Snow1.png").convert(),
        pygame.image.load("tiles/Snow2.png").convert(),
        pygame.image.load("tiles/Snow3.png").convert(),
        pygame.image.load("tiles/Snow4.png").convert(),
    ],
    [
        'rock',
        pygame.image.load("tiles/Rock1.png").convert(),
        pygame.image.load("tiles/Rock2.png").convert(),
        pygame.image.load("tiles/Rock3.png").convert(),
        pygame.image.load("tiles/Rock4.png").convert(),
    ],
    [
        'floor',
        pygame.image.load("tiles/Floor1.png").convert(),
    ],
    [
        'grass',
        pygame.image.load("tiles/Grass1.png").convert(),
        pygame.image.load("tiles/Grass2.png").convert(),
        pygame.image.load("tiles/Grass3.png").convert(),
        pygame.image.load("tiles/Grass4.png").convert(),
        pygame.image.load("tiles/Grass5.png").convert()
    ],
    [
        'planks',
        pygame.image.load("tiles/Wood.png").convert(),
        pygame.image.load("tiles/Wood1.png").convert()
    ],
    [
        'paving',
        pygame.image.load("tiles/Paving.png").convert(),
    ],
    [
        'sand',
        pygame.image.load("tiles/Sand1.png").convert(),
        pygame.image.load("tiles/Sand2.png").convert(),
        pygame.image.load("tiles/Sand3.png").convert(),
        pygame.image.load("tiles/Sand4.png").convert(),
    ],
    [
        'marsh',
        pygame.image.load("tiles/Marsh1.png").convert(),
        pygame.image.load("tiles/Marsh2.png").convert(),
        pygame.image.load("tiles/Marsh3.png").convert(),
        pygame.image.load("tiles/Marsh4.png").convert()
    ],
    [
        'water',
        pygame.image.load("tiles/Water1.png").convert(),
        pygame.image.load("tiles/Water2.png").convert(),
        pygame.image.load("tiles/Water3.png").convert(),
        pygame.image.load("tiles/Water4.png").convert(),
    ],
    [
        'deepwater',
        pygame.image.load("tiles/DeepWater.png").convert()
    ]
]

TerrainIndex = {}
for index in range(0, len(TerrainSprites)):
    entry = TerrainSprites[index]
    TerrainIndex[entry[0]] = index
    entry.pop(0)
    map(lambda x: x.set_colorkey(MAGENTA, pygame.RLEACCEL), entry)
    TerrainSprites[index] = (len(TerrainSprites)/2-index, entry)

# Overlays for unknown, non-visible, damaged or burning tiles.
Unknown = pygame.image.load("tiles/Unknown.png").convert()
NonVisible = pygame.image.load("tiles/NonVisible.png").convert_alpha()

# These two can be randomly chosen
Damaged = [
    pygame.image.load("tiles/Damaged1.png").convert_alpha(),
    pygame.image.load("tiles/Damaged2.png").convert_alpha(),
    pygame.image.load("tiles/Damaged3.png").convert_alpha(),
    pygame.image.load("tiles/Damaged4.png").convert_alpha()

]
Burning = [
    pygame.image.load("tiles/Fire1.png").convert_alpha(),
    pygame.image.load("tiles/Fire2.png").convert_alpha(),
    pygame.image.load("tiles/Fire3.png").convert_alpha(),
    pygame.image.load("tiles/Fire4.png").convert_alpha()
]

# Overlays for fuses.
FuseLeft = pygame.image.load("tiles/Fuse.png").convert_alpha()
FuseRight = pygame.transform.rotate(FuseLeft, 180)
FuseUp = pygame.transform.rotate(FuseLeft, -90)
FuseDown = pygame.transform.rotate(FuseLeft, 90)

Fuse = {
    UP: FuseUp,
    DOWN: FuseDown,
    LEFT: FuseLeft,
    RIGHT: FuseRight
}


# Overlays for tiles with collectables.
Coin = pygame.image.load("tiles/Coin.png").convert_alpha()
Choc = pygame.image.load("tiles/Chocolate.png").convert_alpha()
Dynamite = pygame.image.load("tiles/Dynamite.png").convert_alpha()

Collectables = {
    collectables.COIN: Coin,
    collectables.CHOCOLATE: Choc,
    collectables.DYNAMITE: Dynamite
}

# Player sprites.
PlayerUp = pygame.image.load("tiles/Player.png").convert_alpha()
PlayerDown = pygame.transform.flip(PlayerUp, False, True)
PlayerLeft = pygame.transform.rotate(PlayerUp, 90)
PlayerRight = pygame.transform.flip(PlayerLeft, True, False)

Player = {
    UP: PlayerUp,
    DOWN: PlayerDown,
    LEFT: PlayerLeft,
    RIGHT: PlayerRight
}

# Bear sprites.
BearLeft = pygame.image.load("tiles/Bear.png").convert_alpha()
BearRight = pygame.transform.flip(BearLeft, True, False)

# Dragon sprites.
DragonRedUpLeft = pygame.image.load("tiles/Dragon-Red.png").convert_alpha()
DragonRedUpRight = pygame.transform.flip(DragonRedUpLeft, True, False)
DragonRedDownLeft = pygame.transform.flip(DragonRedUpLeft, False, True)
DragonRedDownRight = pygame.transform.flip(DragonRedUpLeft, True, True)

DragonRed = {
    UPLEFT: DragonRedUpLeft,
    UPRIGHT: DragonRedUpRight,
    DOWNLEFT: DragonRedDownLeft,
    DOWNRIGHT: DragonRedDownRight
}

Sign = pygame.image.load("tiles/Sign.png").convert_alpha()
PixieLeft = pygame.image.load("tiles/Pixie.png").convert_alpha()
PixieRight = pygame.transform.flip(PixieLeft, True, False)

