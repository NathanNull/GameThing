import pygame
from utils import add, mul, lerp, get_collision_sides
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
            if hasattr(spr, "draw"):
                spr.draw(surface)
            else:
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

        self.collides = collides
        
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
    def __init__(self, x, y, img, collide_groups=[], collides=True,\
                 grav=1.75, friction={False:0.9, True:0.8}):
        WorldObject.__init__(self, x, y, img, collides)
        self.vel = (0,0)
        self.acc = (0,0)
        self.collide_groups = collide_groups
        self.collides = collides
        self.grav = grav
        self.friction = friction
        self.grounded = False
        
    def update(self):
        if self.grounded:
            all_sprites = []
            for group in self.collide_groups:
                all_sprites.extend(group.sprites())
            self.grounded = pygame.Rect(self.rect.bottomleft,(self.rect.width,1)).collidelist(all_sprites) != -1
        else:
            self.acc = add(self.acc, (0, self.grav))
        
        self.vel = mul(add(self.vel, self.acc),self.friction[self.grounded])
        self.vel = tuple([round(v, 1) for v in self.vel])

        self.acc = (0,0)

        self.try_move(self.vel, self.collide_groups)

        return super().update()

    def try_move(self, shift, test_groups):
        target_pos = add(self.rect.topleft, shift)
        iterations = max([int(abs(v)) for v in shift])
        
        last_allowed_pos = self.rect.topleft
        for i in range(iterations):
            amount = (i+1)/iterations
            pos = [lerp(a, b, amount) for (a,b) in zip(self.rect.topleft, target_pos)]
            test_rect = pygame.Rect(pos, (self.rect.size))
            passed = True
            for group in test_groups:
                for spr in group.sprites():
                    if hasattr(spr,"collides") and spr.collides\
                    and test_rect.colliderect(spr.rect):
                        sides = get_collision_sides(test_rect, pygame.Rect(last_allowed_pos,self.rect.size), spr.rect)
                        for side in sides:
                            if side in ["left","right"]:
                                self.vel = (0,self.vel[1])
                            elif side in ["top","bottom"]:
                                self.vel = (self.vel[0],0)
                            if side == "bottom":
                                self.grounded = True
                        
                        passed = False
            if not passed:
                break
            last_allowed_pos = test_rect.topleft

        self.rect.topleft = last_allowed_pos

    def push(self, amount):
        self.acc = add(self.acc, amount)