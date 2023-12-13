import pygame
from pygame.math import Vector2
from src.assets.assets import get_font


class Text:
    def __init__(
        self,
        texts: list[str]="",
        pos: Vector2=Vector2(20, 20),
        color: tuple[int, int, int]=(255, 255, 255),
        font_file: str="DroidSansMono.ttf",
        font_size: int=20,
        spacing: int | float=5,
        aa: bool=True,
        bg_color: tuple[int, int, int] | None=None
        ) -> None:
        self.display = pygame.display.get_surface()
        self.texts = texts if type(texts) is list else "change it to list"
        self.pos = pos
        self.color = color
        self.font_file = font_file
        self.spacing = spacing
        self.aa = aa
        self.bg_color = bg_color
        self.font_size = font_size
        self.font = get_font(self.font_file, self.font_size)
    
    def update(
        self, 
        texts: list[str]=None, 
        pos: Vector2=None,
        color: tuple[int]=None,
        font_file: str=None,
        font_size: int=None,
        spacing: int | float=None,
        aa: bool=None,
        bg_color: tuple[int, int, int] | None=None
        ) -> None:
        self._update_texts(texts)
        self._update_pos(pos)
        self._update_color(color)
        self._update_font_file(font_file)
        self._update_font_size(font_size)
        self._update_aa(aa)
        self._update_bg_color(bg_color)
        self._update_spacing(spacing)
    
    def _update_texts(self, texts: list) -> None:
        if self.texts == texts or type(texts) is not list: return
        self.texts = texts
    
    def _update_pos(self, pos: Vector2) -> None:
        if self.pos == pos or pos is None: return
        self.pos = pos.copy()
    
    def _update_color(self, color: tuple[int]) -> None:
        if self.color == color or color is None: return
        self.color = color
    
    def _update_font_file(self, font_file: str) -> None:
        if self.font_file == font_file or font_file is None: return
        self.font_file = font_file
        self.font = get_font(font_file, self.font_size)
    
    def _update_font_size(self, font_size: int) -> None:
        if self.font_size == font_size or font_size is None: return
        self.font_size = font_size
        self.font = get_font(self.font_file, font_size)
    
    def _update_spacing(self, spacing: int | float) -> None:
        if self.spacing == spacing or spacing is None: return
        self.spacing = spacing
    
    def _update_aa(self, aa: bool) -> None:
        if self.aa == aa or aa is None: return
        self.aa = aa
    
    def _update_bg_color(self, bg_color: tuple[int, int, int] | None) -> None:
        if self.bg_color == bg_color or bg_color is None: return
        self.bg_color = bg_color

    def draw(self):
        x_pos = self.pos.x
        y_pos = self.pos.y
        for text in self.texts:
            self.surface = self.font.render(text, self.aa, self.color, self.bg_color)
            self.display.blit(self.surface, [x_pos, y_pos])
            y_pos += self.font_size + self.spacing
