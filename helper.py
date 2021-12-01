# -*- coding: iso-8859-1 -*-

"""
Functions that helps doing image manipulation, etc.
"""

import psp2d


"""
Load a sprite, splitting the image and the shadow
width, height = final width and height of the sprite
"""
def load_sprite(src_file, width, height):
    asset = psp2d.Image('assets/bg-1.png')
    #width = asset.get_width()
    #height = asset.get_height() / 2
    shadow = psp2d.Image(width, height)
    sprite = psp2d.Image(width, height)
    sprite.clear(psp2d.Color(0,0,0,0))
    shadow.blit(asset, 0,height, width, height, 0, 0, True)
    sprite.blit(asset, 0,0, width, height, 0, 0, True)
    return (sprite, shadow)