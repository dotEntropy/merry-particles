import pygame
import time
from src.assets import assets
from src.global_vars import GlobalVars
from src.level import Level


class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Happy Photons")
        pygame.display.set_icon(assets.get_image("icon.png"))
        display_info = pygame.display.Info()
        GlobalVars.client_w = display_info.current_w
        GlobalVars.client_h = display_info.current_h
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self) -> None:
        pre_time = time.time()
        while True:
            dt = time.time() - pre_time
            pre_time = time.time()
            self.level.run(dt)
            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    game = Main()
    game.run()
