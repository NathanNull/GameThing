import pygame
import world
from player import Player
from block import Block, BlockGroup
from pygame.locals import FULLSCREEN, DOUBLEBUF
import gamestates
from config import SCR_SIZE
#for JamisonM: useless = True

#WARNING: doesn't work atm (at least I think so)

# many changes have happened
gamestates.run = True

SCREEN_WIDTH, SCREEN_HEIGHT = SCR_SIZE

pygame.init()
flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode(SCR_SIZE, flags, 16)

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

clock = pygame.time.Clock()
ms = []

GREEN = (102, 255, 102)
text = pygame.font.SysFont('arial', 20)

BlockGroup.generate(45)


player_group = world.WorldGroup()
jesus = Player(100,100,2)
player_group.add(jesus)
jesus.push((10,0))

is_first = True
while gamestates.run:
  pygame.draw.rect(screen,GREEN,((0,0),(SCREEN_WIDTH,SCREEN_HEIGHT)))
  for event in pygame.event.get():
  #quit game
    if event.type == pygame.QUIT:
      gamestates.run = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        world.move((1,0))
    if keys[pygame.K_l]:
        world.move((-1,0))
    if keys[pygame.K_i]:
        world.move((0,-1))
    if keys[pygame.K_m]:
        world.move((0,1))


  
  r = screen.blit(text.render(str(world.screen_world_pos), True, (0,0,0)), (0,0))
  r = pygame.Rect(r.topleft, (200, r.height))

  r = screen.blit(text.render(str(jesus.blocks), True, (0,0,0)), (SCREEN_WIDTH,0))
  r = pygame.Rect(r.topleft, (200, r.height))

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
