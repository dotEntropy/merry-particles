import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import math
from src.assets import assets
from src.utils import vectors
from src.sprites.black_hole import BlackHole


class Particle(Sprite):
    def __init__(
        self,
        pos: Vector2,
        scale: float,
        source: BlackHole,
        ) -> None:
        super().__init__()

        self.pos = pos
        self.accel = Vector2()
        self.accel_mag = 1
        self.source = source
        
        self._update_accel()
        self._init_vel()

        self.IMAGE = assets.get_image("particle.png")
        self.update_image(scale)

    def _init_vel(self) -> None:
        source = self.source
        if source.gravity < 0: self.accel_mag = 1
        self.vel_mag = math.sqrt(self.accel_mag * self.distance)
        self.vel_dir = vectors.get_points_direction(self.pos, source.pos, error=0.2, offset=0.5)
        self.vel: pygame.Vector2 = self.vel_dir * self.vel_mag

    def update_image(self, scale: float) -> None:
        self.scale = scale
        self.image = assets.modify_image(self.IMAGE, scale=self.scale)
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self, dt: float, source: BlackHole) -> None:
        self.source = source
        self._update_accel()
        self._update_vel(dt)
        self._update_pos(dt)
        self._update_vel(dt)

    def _update_accel(self) -> None:
        source = self.source
        self.accel = Vector2()
        self.direction = vectors.get_points_direction(self.pos, source.pos) 
        self.distance = vectors.get_distance(self.pos, source.pos)
        if self.distance == 0: 
            self.kill()
            return
        self.accel_mag = source.gravity * (1 / (self.distance ** 2))
        self.accel += self.direction * self.accel_mag

    def _update_vel(self, dt: float) -> None:
        self.vel += self.accel * 0.5 * dt

    def _update_pos(self, dt: float) -> None:
        self.pos += self.vel * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)
