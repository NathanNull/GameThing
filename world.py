import pygame
from utils import add
from config import SCR_SIZE

screen_world_pos = (0,0)
def move(amount):
    global screen_world_pos
    screen_world_pos = (screen_world_pos[0]+amount[0], screen_world_pos[1]+amount[1])

screen_rect = pygame.Rect((0,0),SCR_SIZE)

class WorldGroup(pygame.sprite.Group):
    # This function is very similar to what it normally is, with some optimizations
    def draw(self, surface, to_draw=None):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if not spr.screen_rect.colliderect(screen_rect):
                continue
            #before: self.spritedict[spr] = surface_blit(spr.image, spr.rect)
            self.spritedict[spr] = surface_blit(spr.image, spr.screen_rect)
            
        self.lostsprites = []

    # So is this function, but this time it's modified to return details about
    # sprites that have changed
    def update(self, *args):
        #before:
        #for s in self.sprites():
        #    s.update(*args)
        
        changed_rects = []
        
        for s in self.sprites():
            r_val = s.update(*args)
            if r_val != None:
                changed_rects.append(r_val)
                
        return changed_rects

class WorldObject(pygame.sprite.Sprite):
    def __init__(self, x, y, img, collides=True):
        pygame.sprite.Sprite.__init__(self)
        
        self.x, self.y = x, y
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self._last_scr_pos = self.screen_rect

    # Return this at the end of your custom update function, otherwise it won't draw
    def update(self):
        if self._last_scr_pos != self.screen_rect:
            lsp = self._last_scr_pos
            self._last_scr_pos = self.screen_rect
            
            r = pygame.Rect.union(lsp, self.screen_rect)
            if r.colliderect(screen_rect):
                return r

    @property
    def screen_rect(self):
        return pygame.Rect(\
            self.rect[0]-screen_world_pos[0], self.rect[1]-screen_world_pos[1],\
            self.rect[2], self.rect[3]\
        )

    @screen_rect.setter
    def screen_rect(self, val):
        self.rect = pygame.Rect(\
            val[0]+screen_world_pos[0], val[1]+screen_world_pos[1],\
            val[2], val[3]\
        )

    # def draw(self, surface):
    #     pass

class PhysicsObject(WorldObject):
    def __init__(self, x, y, img, collides=True,\
                 grav=1, friction={"air":0.9, "ground":0.8}):
        WorldObject.__init__(self, x, y, img, collides)
        self.vel = (0,0)
        self.acc = (0,0)
        self.grav = grav
        
    def update(self):
        self.acc = add(self.acc, (0, self.grav))
        
        self.vel = add(self.vel, self.acc)

        self.acc = (0,0)

        self.try_move(self.vel)

        return super().update()

    def try_move(self, amount):
        self.rect.center = add(self.rect.center, amount)

    def push(self, amount):
        self.acc = add(self.acc, amount)