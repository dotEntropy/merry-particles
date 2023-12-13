import pygame
from pygame.event import Event
from pygame.math import Vector2
import sys
from src.utils.text import Text
from src.sprites.black_hole import BlackHole
from src.sprites.particle import Particle


class Level:
    def __init__(self) -> None:
        self._init_display()
        self._init_sprites()
        self._init_config()
        self._init_texts()

    def _init_display(self) -> None:
        self.WIN = pygame.display.get_surface()
        self.BG_COLOR = (0, 0, 0)

    def _init_sprites(self) -> None:
        self.source_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        self.black_hole = BlackHole(groups=self.source_group)
    
    def _init_config(self) -> None:
        self.particle_scale = 0.05
        self.trickle_particles = False

    def _init_texts(self) -> None:
        self.black_hole_texts = Text()

    # LOOP

    def run(self, dt: float) -> None:
        self._events()
        self._update(dt)
        self._draw()

    # EVENTS

    def _events(self) -> None:
        self.mouse_pos = Vector2(*pygame.mouse.get_pos())

        mouse_buttons = pygame.mouse.get_pressed()
        self._spray_particles(mouse_buttons)

        keys = pygame.key.get_pressed()
        self.black_hole.update_direction(keys)

        for event in pygame.event.get():
            self._handle_mouse_controls(event)
            self._handle_key_controls(event)
            self._quit_event(event)

    def _spray_particles(self, mouse_buttons: tuple) -> None:
        if mouse_buttons[0] and not self.trickle_particles:
            self.spawn_particle()
    
    def spawn_particle(self) -> None:
        particle = Particle(
            self.mouse_pos,
            self.particle_scale,
            self.black_hole,
            )
        self.particle_group.add(particle)

    def _handle_key_controls(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN: return

        if event.key == pygame.K_t:
            self.trickle_particles = not(self.trickle_particles)
        if event.key == pygame.K_SPACE:
            self._clear_all_particles()

        if event.key == pygame.K_UP:
            self._increase_gravity()
        if event.key == pygame.K_DOWN:
            self._decrease_gravity()
        if event.key == pygame.K_n:
            self._invert_gravity()

    def _clear_all_particles(self) -> None:
        for particle in self.particle_group:
            particle.kill()
    
    def _increase_gravity(self) -> None:
        gravity = self.black_hole.gravity
        if not gravity:
            gravity = 10
        elif gravity == -10:
            gravity = 0 
        elif gravity < 0:
            gravity //= 10
        else: 
            gravity *= 10
        for source in self.source_group:
            source.gravity = gravity
        
    def _decrease_gravity(self) -> None:
        gravity = self.black_hole.gravity
        if not gravity:
            gravity = -10
        elif gravity == 10: 
            gravity = 0
        elif gravity < 0: 
            gravity *= 10
        else: 
            gravity //= 10
        for source in self.source_group:
            source.gravity = gravity
    
    def _invert_gravity(self) -> None:
        self.black_hole.gravity *= -1

    def _handle_mouse_controls(self, event: Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN: return

        if event.button == 1 and self.trickle_particles:
            self.spawn_particle()
        if event.button == 4:
            self._increase_particle_scale()
        if event.button == 5:
            self._decrease_particle_scale()

    def _increase_particle_scale(self) -> None:
        self.particle_scale = min(round(self.particle_scale + 0.05, 2), 1.0)
        for particle in self.particle_group:
            particle.update_image(self.particle_scale)

    def _decrease_particle_scale(self) -> None:
        self.particle_scale = max(round(self.particle_scale - 0.05, 2), 0.05)
        for particle in self.particle_group:
            particle.update_image(self.particle_scale)

    @staticmethod
    def _quit_event(event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN: return
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # UPDATE

    def _update(self, dt: float) -> None:
        self.particle_group.update(dt, self.black_hole)
        self.source_group.update(dt)

        # check devoured particles
        for particle in self.particle_group:
            if particle.distance - self.black_hole.radius > 0: continue
            particle.kill()
            self.black_hole.devoured_quantity += 1
        
        self.black_hole_texts.update(texts=[
            f"Particles Devoured: {self.black_hole.devoured_quantity}",
            f"Gravity: {self.black_hole.gravity}",
            f"Number of Particles: {len(self.particle_group)}",
            f"Particle Scale: {self.particle_scale}x",
            "",
            "[N] Invert Gravity",
            "[T] Toggle Spray",
            "[SCRL UP] Scale Up Particles",
            "[SCRL DOWN] Scale Down Particles",
            "[SPACE] Clear Particles"
            ])

    # DRAW

    def _draw(self) -> None:
        self.WIN.fill(self.BG_COLOR)
        self.particle_group.draw(self.WIN)
        self.source_group.draw(self.WIN)
        self.black_hole_texts.draw()
