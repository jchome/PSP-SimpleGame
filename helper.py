# -*- coding: iso-8859-1 -*-

"""
Functions that helps doing image manipulation, etc.
"""

from psp2d import Image, Color

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

class Rect(Point):
    def __init__(self, x, y, w, h):
        Point.__init__(self, x, y)
        self.w = w
        self.h = h
    def __str__(self):
        return "Rect(%d, %d, %d, %d)" % (self.x, self.y, self.w, self.h)

    def top_left(self):
        return Point(self.x, self.y)

    def top_right(self):
        return Point(self.x + self.w, self.y)

    def bottom_left(self):
        return Point(self.x, self.y + self.h)
    
    def bottom_right(self):
        return Point(self.x + self.w, self.y + self.h)


"""
Load a sprite, splitting the image and the shadow
width, height = final width and height of the sprite
"""
def load_sprite(src_file, width, height):
    try:
        asset = Image(src_file)
    except:
        print("Error while loading file %s" % src_file)
    #width = asset.get_width()
    #height = asset.get_height() / 2
    shadow = Image(width, height)
    sprite = Image(width, height)
    sprite.clear(Color(0,0,0,0))
    shadow.blit(asset, 0,height, width, height, 0, 0, True)
    sprite.blit(asset, 0,0, width, height, 0, 0, True)
    return (sprite, shadow)

def collision_on_rectangles(rect1, rect2):
    if rect1.x < rect2.x+rect2.w and rect1.x+rect1.w > rect2.x:
        if rect1.y < rect2.y+rect2.h and rect1.y+rect1.h > rect2.y:
            return True
    return False

def point_in_rect(point, rect):
    if point.x < rect.x + rect.w and point.x > rect.x:
        if point.y < rect.y + rect.h and point.y > rect.y:
            return True
    return False

def match_one_color(list_of_colors, color2):
    for color1 in list_of_colors:
        if match_colors(color1, color2):
            return True
    return False

def match_colors(color1, color2):
    if color1.red == color2.red and color1.green == color2.green and color1.blue == color2.blue:
        return True
    else:
        return False

## test
if __name__ == "__main__":
    point_5_5 = Point(5,5)
    print( "point(10,8) in Rect(5,5,10,20) ? True ==> %r" % point_in_rect(Point(10,8), Rect(5,5,10,20)) )
    ## Left
    print( "point(2,10) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(2,10), Rect(5,5,10,20)) )
    ## Top left
    print( "point(2,2) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(2,2), Rect(5,5,10,20)) )
    ## Top
    print( "point(2,20) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(2,20), Rect(5,5,10,20)) )
    ## Top Right
    print( "point(4,40) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(4,40), Rect(5,5,10,20)) )
    ## Right
    print( "point(10,40) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(10,40), Rect(5,5,10,20)) )
    ## Bottom Right
    print( "point(20,40) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(20,40), Rect(5,5,10,20)) )
    ## Bottom
    print( "point(20,10) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(20,10), Rect(5,5,10,20)) )
    ## Bottom Left
    print( "point(20,2) in Rect(5,5,10,20) ? False ==> %r" % point_in_rect(Point(20,2), Rect(5,5,10,20)) )