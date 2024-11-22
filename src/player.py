import pygame
from settings import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, sem_collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.direction = pygame.math.Vector2()
        self.speed = 30  # Increased speed for noticeable movement
        self.gravity = 15
        self.jump = False
        self.jump_height = 100

        self.sem_collision_sprites = sem_collision_sprites
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        self.display_surface = pygame.display.get_surface()

        # timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = pygame.math.Vector2(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT]:
                input_vector.x += 1
            if keys[pygame.K_LEFT]:
                input_vector.x -= 1
            self.direction.x = input_vector.normalize().x if input_vector.x else input_vector.x
        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        # Move the player horizontally
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Apply gravity and move the player vertically
        if not self.on_surface['floor'] and any([self.on_surface['left'], self.on_surface['right']]) and not \
        self.timers['wall slide block'].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 2 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')
        self.semi_collision()
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
            elif any([self.on_surface['left'], self.on_surface['right']]):
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

    def platform_move(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt
            if self.platform.direction.y != 0:
                self.on_surface['floor'] = True
                self.direction.y = 0


    def check_contact(self):
        floor_rect = pygame.Rect((self.rect.bottomleft), (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + pygame.math.Vector2(0, self.rect.height / 4),
                                 (2, self.rect.height / 2))
        left_rect = pygame.Rect((self.rect.topleft + pygame.math.Vector2(-2, self.rect.height) / 4),
                                (2, self.rect.height / 2))
        semi_collision_rect = [sprite.rect for sprite in self.sem_collision_sprites]
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_surface['floor'] = any([
            floor_rect.collidelist(collide_rects) >= 0,
            floor_rect.collidelist(semi_collision_rect) >= 0 and self.direction.y >= 0
        ])

        self.on_surface['right'] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(collide_rects) >= 0

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.sem_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if self.rect.colliderect(floor_rect):
                self.platform = sprite
                self.on_surface['floor'] = True
                # Nếu platform di chuyển lên, điều chỉnh hướng y để phù hợp
                if hasattr(sprite, 'direction') and sprite.direction.y < 0:
                    self.direction.y = sprite.direction.y * sprite.speed

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def semi_collision(self):
        for sprite in self.sem_collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0



    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timer()
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        print(self.on_surface)
