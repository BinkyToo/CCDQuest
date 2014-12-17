import numpy
import pygame.surfarray

import images

celltypefields = [
    ('name',           (numpy.str_, 19)),
    ('top',             numpy.bool_),
    ('destructable',    numpy.bool_),
    ('temperature',     numpy.int8 ),
    ('fireignitechance',numpy.float_),
    ('fireoutchance',   numpy.float_),
    ('hasroof',         numpy.bool_),
    ('difficulty',      numpy.int8 ),
    ('transparent',     numpy.bool_),
    ('solid',           numpy.bool_),
    ('sogginess',       numpy.uint8)
]

csvcolorfields = [
    ('r',               numpy.uint8),
    ('g',               numpy.uint8),
    ('b',               numpy.uint8)
]

csvimagefields = [
    ('groundimage',    (numpy.str_, 20)),
    ('topimage',       (numpy.str_, 20))
]

csvdtype = numpy.dtype(csvcolorfields + celltypefields + csvimagefields)

types = numpy.genfromtxt('map/terrain.csv', delimiter=',', dtype=csvdtype, autostrip=True)
typeslist = types.tolist()

def colorlist(surface):
    return pygame.surfarray.map_array(surface, types[['r','g','b']].view(numpy.uint8).reshape(-1, 3))
def color_typeindex(surface):
    return zip(colorlist(surface), range(len(typeslist)))

typeimages = []
for type in types:
    typeimages.append((
        images.terrain[type['groundimage']],
        images.terrain[type['topimage']]
        ))

cellstatefields = [
    ('damaged',         numpy.bool_),
    ('explored',        numpy.bool_),
    ('collectableitem', numpy.int8)
]

cellimagefields = [
    ('layeroffset',     numpy.int_),
    ('groundimage',     numpy.object),
    ('topimage',        numpy.object)
]

celldtype = numpy.dtype(cellstatefields + celltypefields + cellimagefields)

def copyfill(i):
    colorlen = len(csvcolorfields)
    layeroffset = (len(types)/2-i[0],)
    return (0,)*len(cellstatefields) + i[1][colorlen:colorlen+len(celltypefields)] + layeroffset + typeimages[i[0]]
typeindextocell = numpy.array([copyfill(i) for i in enumerate(typeslist)], dtype=celldtype)
