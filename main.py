import pygame
import world
import block
from player import Player
from pygame.locals import FULLSCREEN, DOUBLEBUF
from config import SCR_SIZE
#for JamisonM: useless = True

# many changes have happened

SCREEN_WIDTH, SCREEN_HEIGHT = SCR_SIZE

pygame.init()
flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode(SCR_SIZE, flags, 16)

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

clock = pygame.time.Clock()
ms = []

GREEN = (102, 255, 102)
text = pygame.font.SysFont('arial', 20)

block.generate(45)

jesus = Player(100,100,2)
player_group = world.WorldGroup()
player_group.add(jesus)
jesus.push((10,0))

run = True
is_first = True
while run:
  for event in pygame.event.get():
  #quit game
    if event.type == pygame.QUIT:
      run = False

    if event.type == pygame.KEYDOWN:
      print('You pressed a button! Good job')
      if event.key == pygame.K_a:
        print("You pressed A! I'm so proud")
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        world.move((1,0))
    if keys[pygame.K_l]:
        world.move((-1,0))
    if keys[pygame.K_i]:
        world.move((0,-1))
    if keys[pygame.K_m]:
        world.move((0,1))


  pygame.draw.rect(screen,GREEN,((0,0),(SCREEN_WIDTH,SCREEN_HEIGHT)))
  r = screen.blit(text.render(str(world.screen_world_pos), True, (0,0,0)), (0,0))
  r = pygame.Rect(r.topleft, (100, r.height))

  rects = [r]

  rects.extend(player_group.update())
  player_group.draw(screen)

  rects.extend(block.all_blocks.update())
  block.all_blocks.draw(screen)

  pygame.draw.rect(screen,GREEN,((SCREEN_WIDTH,SCREEN_HEIGHT),(0,0)))

  dt = clock.tick(30)
  ms.append(dt)
  if sum(ms)>1000:
    fps = [1/(t/1000) for t in ms]
    #print(round(sum(fps)/len(fps), 2))
    ms = []

  if is_first:
    pygame.display.update()
    is_first = False
  else:
    pygame.display.update(rects)

pygame.quit()
