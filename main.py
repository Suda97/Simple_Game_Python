import pygame
from pygame.locals import *
import sys
import random

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

frame_per_sec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')


class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((147, 50, 168))
        self.rect = self.surf.get_rect()

        self.pos = vec((15, 430))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC

        if pressed_keys[K_SPACE]:
            self.jump()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x >= WIDTH:
            self.pos.x = WIDTH
        if self.pos.x <= 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

        if self.pos.y > HEIGHT:
            self.die()

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15

    def collision(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def die(self):
        pygame.quit()
        sys.exit()


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super(platform, self).__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((128, 128, 128))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))


def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = platform()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)


PT1 = platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 1))
P1 = player()

platforms = pygame.sprite.Group()
platforms.add(PT1)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

for i in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)

    pygame.display.update()
    frame_per_sec.tick(FPS)
    plat_gen()
    P1.collision()
    P1.move()

