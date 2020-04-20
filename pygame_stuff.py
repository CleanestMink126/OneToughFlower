import pygame
import os
from constants import HIGHLIGHTER, SELECTOR, BACKGROUNDS, MIDDLE, TOP


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class PygameHandler:
    def __init__(self, tile_size):
        self.levels = [BACKGROUNDS, MIDDLE, TOP]
        self.lcm = 1
        self.make_tiles(tile_size)
        self.make_highlighter(tile_size)
        self.make_text()
        self.shakex = 0
        self.shakey = 0

    def make_highlighter(self, tile_size):
        full_path = os.path.join(HIGHLIGHTER)
        img = pygame.image.load(full_path)
        self.highlight = pygame.transform.scale(img, tile_size)
        full_path = os.path.join(SELECTOR)
        img = pygame.image.load(full_path)
        self.select = pygame.transform.scale(img, tile_size)

    def make_text(self):
        size = 20
        self.font = pygame.font.SysFont("monospace", size)
        self.title = pygame.font.SysFont("monospace", 30)
        self.intro = pygame.font.SysFont("monospace", 25)

    def make_tiles(self, tile_size):
        """this will add all the of required images to variables so they are accessable
        and will adjust them to the correct size"""
        self.tile_img_levels = []
        for i, level in enumerate(self.levels):

            d = {}
            for name, l in level.items():
                if i == 0:
                    img_dict = {}
                    for k, v in l.items():
                        imgs = []
                        for path in v:
                            full_path = os.path.join(path)
                            img = pygame.image.load(full_path)
                            img = pygame.transform.scale(img, tile_size)
                            imgs.append(img)
                        img_dict[k] = imgs
                    d[name] = img_dict

                else:
                    imgs = []
                    for path in l:
                        full_path = os.path.join(path)
                        img = pygame.image.load(full_path)
                        img = pygame.transform.scale(img, tile_size)
                        imgs.append(img)
                    d[name] = imgs
                    if (self.lcm % len(imgs)):
                        self.lcm *= len(imgs)
            self.tile_img_levels.append(d)

    def render_tile(self, screen, levels, image_info, location, count):
        for i, level_dict in enumerate(self.tile_img_levels):
            type = levels[i]
            if type is None:
                continue
            if i == 0:
                array, rotation = image_info
                img_dict = level_dict[type]
                img_list = img_dict[array]
                offset = count % len(img_list)
                if len(img_list) > 1:
                    # print(location)
                    # print(hash(location))
                    r = hash(str(location[0]) + str(location[1]))
                    offset = (count + r) % len(img_list)
                img = img_list[offset]
                img = pygame.transform.rotate(img, rotation)
            else:
                img_list = level_dict[type]
                img = img_list[count % len(img_list)]
            screen.blit(img, self.shake(location))

    def shake(self, loc):
        return loc[0] + self.shakex, loc[1] + self.shakey

    def render_highlight(self, screen, location):
        screen.blit(self.highlight, self.shake(location))

    def render_select(self, screen, location):
        screen.blit(self.select, self.shake(location))

    def render_text_center(self, screen, text, location):
        score = self.intro.render(text, 1, (248, 255, 184))
        loc = score.get_rect(center=location)
        screen.blit(score, self.shake(loc))

    def render_title(self, screen, text, screen_size):
        purp = 66, 0, 78

        score = self.title.render(text, 1, (248, 255, 184), purp)
        loc = score.get_rect(center=(screen_size[0]/2, screen_size[1]/2))

        screen.blit(score, self.shake(loc))

    def render_text(self, screen, text, location):
        score = self.font.render(text, 1, (248, 255, 184))
        screen.blit(score, self.shake(location))
