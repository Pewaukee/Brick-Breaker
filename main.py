# run from python interpreter 3.9.0 32 bit, otherwise pygame will not be found

import collections
import math
import pygame

from random import randint

from levels import *

pygame.init()

# to make the game render at 30 frames per second, 
# which helps to minimize the infinite loop running amount
FPS = 60


class Player(object):
    def __init__(self) -> None:
        self.WIDTH, self.HEIGHT = 800, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Brick Breaker")

        # use of switch statement before python 3.10,
        # check here: https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
        self.levels = {
            1: level1,
            2: level2,
            3: level3
        }
        
        # Rect(x, y, width, height)
        # the bar cannot be moved up or down
        self.sliding_bar = pygame.Rect(350,700,80,10)

        midpoint = (350+350+80)/2-15/2 # put the ball in the center of sliding bar
        self.ball = pygame.Rect(midpoint, 685, 15, 15)
        # seperate ball velocity into 2 parts
        self.angle = 45
        self.ball_x_velocity = 5
        self.ball_y_velocity = -5

        self.WHITE = (255,255,255)
        self.BLACK = (0, 0, 0)
        self.PINK = (245, 66, 221)
        self.LIGHT_BLUE = (101, 178, 207)

        self.BRICK_WIDTH, self.BRICK_HEIGHT = 50, 25
        self.level = 0
        self.bricks = []
        self.colors = []

    def make_bricks(self) -> None:
        # updates and sees if all the bricks are deleted, then move on to next level
        if len(self.bricks) == 0:
            if self.level == 3: # the game is over as this is highest level
                exit("You've completed the game, congrats!")
            self.level+=1
            return_dict = self.levels[self.level]() # equivalent of switch statement for calling funcs
            
            self.bricks = list(return_dict.keys())
            for i in range(len(self.bricks)):
                self.bricks[i] = pygame.Rect(self.bricks[i][0], self.bricks[i][1], self.bricks[i][2], self.bricks[i][3])

            self.colors = list(return_dict.values())
        
    def draw_objects(self) -> None:
        # draw the sliding bar, ball, and also the bricks

        # need to fill screen in order to refresh rectangles
        self.WIN.fill(self.BLACK)
        for i in range(len(self.bricks)):
            pygame.draw.rect(self.WIN, self.colors[i], pygame.Rect(self.bricks[i])) # brick is a tuple of the required characteristics
        pygame.draw.rect(self.WIN, self.PINK, self.sliding_bar, border_radius=10)
        pygame.draw.rect(self.WIN, self.LIGHT_BLUE, self.ball, border_radius=5)


    def move_ball(self) -> None:
        # move the ball according to its velocity
        
        # convert degrees to radians and move ball the correct direction
        self.ball.x += self.ball_x_velocity*math.cos(self.angle*math.pi/180)
        self.ball.y += self.ball_y_velocity*math.sin(self.angle*math.pi/180)

    def handle_collisions(self) -> None:
        # check if the ball has collided with the sliding bar, edge of screen, or bricks
        if self.ball.colliderect(self.sliding_bar):
            # if there is a collision with the bar, make a new random angle for the ball to travel
            # angle bounds between 20 and 80 degrees
            
            # only have a correct collision if the top of bar is close enough to bottom of ball, preventing side collisions
            if abs(self.sliding_bar.top - self.ball.bottom) < 5:
                self.angle = randint(20,80)
                # also deflect the ball (reverse y velo)
                self.ball_y_velocity *= -1

            return # if collided with bar, it can't be colliding with bricks too

        # set the collision tolerance in order to match how much the ball moves per second
        # using pythagorean thereoem
        collision_tolerance = pow(pow(self.ball_x_velocity, 2) + pow(self.ball_y_velocity, 2), 0.5)
        
        # check collision with bricks, and delete
        # use a while loop to delete mid loop
        i = 0
        while i < len(self.bricks):
            if self.ball.colliderect(self.bricks[i]):
                if abs(self.bricks[i].top - self.ball.bottom) <= collision_tolerance:
                    self.ball_y_velocity *= -1
                if abs(self.bricks[i].bottom - self.ball.top) <= collision_tolerance:
                    self.ball_y_velocity *= -1
                if abs(self.bricks[i].right - self.ball.left) <= collision_tolerance:
                    self.ball_x_velocity *= -1
                if abs(self.bricks[i].left - self.ball.right) <= collision_tolerance:
                    self.ball_x_velocity *= -1

                # if there is a collision, delete the brick   
                del self.bricks[i]
                del self.colors[i]
                break # only delete one brick at a time
            i+=1

        if self.ball.y < 0 or self.ball.y > self.HEIGHT-15:
            self.ball_y_velocity *= -1
        if self.ball.x < 0 or self.ball.x > self.WIDTH-15:
            self.ball_x_velocity *= -1

    def update_window(self) -> None:
        pygame.display.update()

    def handle_keys_pressed(self) -> None:
        # handles the movement of the sliding bar

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: # left arrow pressed
            if self.sliding_bar.x >= 10: 
                self.sliding_bar.move_ip(-10,0) # move bar 10 pixels to left
            if self.sliding_bar.x < 10: self.sliding_bar.x = 0
        if key[pygame.K_RIGHT]: # right arrow pressed
            if self.sliding_bar.x <= self.WIDTH - self.sliding_bar.width: 
                self.sliding_bar.move_ip(10,0) # move bar 10 pixels to right
            if self.sliding_bar.x > self.WIDTH - self.sliding_bar.width:
                self.sliding_bar.x = self.WIDTH - self.sliding_bar.width

def main() -> None:
    player = Player()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.make_bricks()
        player.move_ball()
        player.handle_collisions()
        player.draw_objects()
        player.handle_keys_pressed()
        player.update_window()
    
    pygame.quit()

if __name__ == '__main__':
    main()