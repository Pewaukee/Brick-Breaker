# make the levels in the game (1-5)
from random import random, randrange


WIDTH, HEIGHT = 800, 800 # for centering purposes of bricks

BRICK_WIDTH, BRICK_HEIGHT = 75, 25
# for each level, return a 2d array as the set of x and y coords for all the bricks

# get a random color for the rectangle
def random_color() -> tuple:
    satisfy_no_black = False
    while not satisfy_no_black:
        color = tuple([randrange(0,255) for _ in range(3)])
        # make sure color is not black
        for rbg in color:
            if rbg > 25: # arbitrary to say there is at least some color
                satisfy_no_black = True
                break
    return color

def level1() -> dict:
    res = {}
    for i in range(6):
        for j in range(4):
            res[(25 + (50 + BRICK_WIDTH)*i, 
                25 + (50 + BRICK_HEIGHT)*j, BRICK_WIDTH, BRICK_HEIGHT)] = random_color()

    return res

def level2() -> dict:
    midpoint_x = WIDTH / 2 - BRICK_WIDTH / 2
    starting_y = 150
    res = {(midpoint_x, starting_y, BRICK_WIDTH, BRICK_HEIGHT): random_color()}
    for i in range(3):
        for j in range(3):
            # add a rectangle in all 4 directions: up and down, left and right
            res[(midpoint_x + (25 + BRICK_WIDTH)*i, 
                starting_y + (25 + BRICK_HEIGHT)*j, 
                BRICK_WIDTH, BRICK_HEIGHT)] = random_color()
            res[(midpoint_x - (25 + BRICK_WIDTH)*i, 
                starting_y - (25 + BRICK_HEIGHT)*j, 
                BRICK_WIDTH, BRICK_HEIGHT)] = random_color()
            res[(midpoint_x - (25 + BRICK_WIDTH)*i, 
                starting_y + (25 + BRICK_HEIGHT)*j, 
                BRICK_WIDTH, BRICK_HEIGHT)] = random_color()
            res[(midpoint_x + (25 + BRICK_WIDTH)*i, 
                starting_y - (25 + BRICK_HEIGHT)*j, 
                BRICK_WIDTH, BRICK_HEIGHT)] = random_color()
            
    return res

def level3() -> dict:
    res = {}
    for i in range(4):
        for j in range(int(WIDTH/BRICK_WIDTH)):
            res[(25 + BRICK_WIDTH*j, 50 + BRICK_HEIGHT*i, BRICK_WIDTH, BRICK_HEIGHT)] = random_color()

    return res
