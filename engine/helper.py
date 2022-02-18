# -*- coding: iso-8859-1 -*-

"""
Functions that helps doing image manipulation, etc.
"""

from psp2d import Image, Color

class Point(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    """
    Create a copy of this point to update x and y values
    """
    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

class Rect(Point):
    def __init__(self, x, y, w, h):
        Point.__init__(self, x, y)
        self.w = int(w)
        self.h = int(h)
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
    sprite = Image(width, height)
    sprite.clear(Color(0,0,0,0))
    sprite.blit(asset, 0,0, width, height, 0, 0, True)
 
    shadow = Image(width, height)
    shadow.clear(Color(0,0,0,0))
    shadow.blit(asset, 0,height, width, height, 0, 0, True)
    
    return (sprite, shadow)

"""
Returns True if the both rectangles are in collision
"""
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
    if color1 is None or color2 is None:
        return False
    if color1.red == color2.red and color1.green == color2.green and color1.blue == color2.blue:
        return True
    else:
        return False
        
def color_not_alpha_0(list_of_colors):
    for color in list_of_colors:
        if color.alpha != 0:
            return color
    return None

"""
Convert a color as String
"""
def str_color(color):
    return "Color(%d,%d,%d, %d)" % (color.red, color.green, color.blue, color.alpha)

class FontHelper:
    all_width = {"!": 5, '\"': 6, "#": 10, "$": 8, "%": 13, "&": 10, "\'": 3, "(": 5, ")": 5, "*": 7,
        "+": 9, ",": 4, "-": 6, ".": 3, "/": 7, "0": 8, "1": 7, "2": 8, "3": 8, "4": 9, "5": 8, "6": 8, "7": 8, "8": 8, "9": 8, 
        ":": 3, ";": 4, "<": 9, "=": 9, ">": 9, "?": 7, "@": 12,
        "A": 10, "B": 8, "C": 9, "D": 9, "E": 8, "F": 8, "G": 9, "H": 9, "I": 5, "J": 6, "K": 8, "L": 8, "M": 10, "N": 9,
        "O": 8, "P": 8, "Q": 10, "R": 9, "S": 8, "T": 8, "U": 9, "V": 10, "W": 13, "X": 8, "Y": 9, "Z" : 8,
        "[": 5, "\\": 7, "]": 5, "^": 10, "_": 10, "`": 4,
        "a": 8, "b": 8, "c": 7, "d": 8, "e": 8, "f": 6, "g": 8, "h": 8, "i": 3, "j": 5, "k": 7, "l": 3, "m": 11, "n": 8, 
        "o": 8, "p": 8, "q": 8, "r": 6, "s": 7, "t": 7, "u": 8, "v": 7, "w": 11, "x": 7, "y": 7, "z": 7
    }

    @staticmethod
    def width_for_text(text):
        width = 0
        for letter in text:
            if letter  not in FontHelper.all_width:
                ## default width
                width += 8
            else:
                width += FontHelper.all_width[letter]
        return width

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