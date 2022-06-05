import pygame
import world

rand_sprite = 'sprites/0.png'

class Player(world.PhysicsObject):
  def __init__(self, x , y, scale):
    super().__init__(x, y, pygame.image.load(rand_sprite))
    self.speed = 10

  def move(self, moving_left, moving_right):
    #reset movement variables
    dx = 0
    dy = 0
    
    #Assign movement variable
    if moving_left:
        dx = -self.speed
        self.flip = True
        self.direction = -1
    if moving_right:
        dx = self.speed
        self.flip = False
        self.direction = 1

    self.rect.x += dx
    self.rect.y += dy