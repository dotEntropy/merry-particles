import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.global_vars import GlobalVars
from src.assets import assets


class BlackHole(Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group
        ) -> None:
        super().__init__(groups)

        self.pos = Vector2(GlobalVars.client_w/2, GlobalVars.client_h/2)
        self.speed = 250
        self.vel = Vector2()
        self.direction = Vector2()
        self.gravity = 1_000_000
        self.devoured_quantity = 0

        self.IMAGE = assets.get_image("black-hole.png", scale=1)
        self.image = self.IMAGE
        self.diameter = (self.image.get_width() + self.image.get_height()) / 2
        self.radius = self.diameter / 2
        self.rect = self.image.get_rect(center=self.pos)

    def update_direction(self, keys: dict) -> None:
        self.direction = Vector2()
        if keys[pygame.K_w]:
            self.direction.y -= 1
        if keys[pygame.K_s]:
            self.direction.y += 1
        if keys[pygame.K_a]:
            self.direction.x -= 1
        if keys[pygame.K_d]:
            self.direction.x += 1
        if self.direction: 
            self.direction.normalize_ip()
        self.vel = self.speed * self.direction

    def update(self, dt: float) -> None:
        self._update_pos(dt)

    def _update_pos(self, dt: float) -> None:
        self.pos += self.vel * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
