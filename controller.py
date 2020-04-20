from board import Board
from constants import (TOTAL_SIZE, BOARD_SIZE, BOARD_SIZE_PX, BORDER_WIDTH,
                       TYPES, FLOWERS, ROUNDS, BACKGROUNDS, MIDDLE, TOP, LAVA_ERUPT, LAVA_THREAT, DOGSONG)
from pygame_stuff import PygameHandler
from image_stuff import get_dir_dict
from audio_controller import AudioController
import pygame
import numpy as np


class Controller:

    def __init__(self):
        channels = 10
        self.audio_controller = AudioController(8)
        self.board = Board(self.audio_controller)
        self.board_size = self.board.board_size
        self.board_size_px = BOARD_SIZE_PX
        self.tile_size = BOARD_SIZE_PX[0] // BOARD_SIZE[0], BOARD_SIZE_PX[1] // BOARD_SIZE[1]
        # Define Handler
        self.pygame_handler = PygameHandler(self.tile_size)

        # Animation
        self.lcm = self.pygame_handler.lcm
        self.animation_cnt = 0
        # Highlighter
        self.old_loc = None
        self.hloc = [0, 0]
        self.curr_type = 0
        self.flower_idx = 0
        # Menu
        base_loc = BORDER_WIDTH + self.board_size[0] * self.tile_size[0], BORDER_WIDTH + self.tile_size[1]
        self.type_locations = [(base_loc[0], base_loc[1] + self.tile_size[0] * i) for i in range(len(FLOWERS))]
        self.cost_locations = [(loc[0] + self.tile_size[0] + BORDER_WIDTH, loc[1] +
                                self.tile_size[0] / 4.0) for loc in self.type_locations]
        self.bottom_loc = BORDER_WIDTH, BORDER_WIDTH + self.board_size[1] * self.tile_size[1]
        self.seed_loc = BORDER_WIDTH + self.board_size[0] * self.tile_size[0], BORDER_WIDTH
        # Game Stuff
        self.round_started = False
        self.round = 0
        self.steps_until_lava = 15
        self.steps = 0
        self.lose = False
        self.dir_dict = get_dir_dict()
        # Set tiles for initial board
        self.board.set_tile(3, (self.board_size[0]//2, self.board_size[1]//2))
        self.seeds = 20
        self.costs = [5, 5, 10, 10, 10, 10, 20]
        self.seed_prod = 5

    def start_round(self):
        if self.round_started:
            return 0
        self.round_started = True
        self.audio_controller.start_threat()
        self.board.threaten_lava_outbreak(ROUNDS[self.round][1])
        return 1

    def check_in_screen(self, pos):
        return (pos[0] < 0 or pos[0] > TOTAL_SIZE[0]) or (pos[1] < 0 or pos[1] > TOTAL_SIZE[1])

    def check_in_board(self, pos):
        return (pos[0] < self.board_size_px[0]) and (pos[1] < self.board_size_px[1])

    def check_in_sidebar(self, pos):
        tl = self.type_locations[0]
        in_x = (pos[0] >= tl[0] and pos[0] < (tl[0] + self.tile_size[0]))
        in_y = (pos[1] >= tl[1] and pos[1] < (tl[0] + len(FLOWERS) * self.tile_size[0]))
        return in_x and in_y

    def handle_mouse(self, pos):
        # Check bounds
        if self.check_in_screen(pos):
            return
        elif self.check_in_board(pos):
            self.hloc = [pos[0] // self.tile_size[0], pos[1] // self.tile_size[1]]

    def click(self, pos):
        if self.check_in_screen(pos):
            return
        elif self.check_in_board(pos):
            self.hloc = [pos[0] // self.tile_size[0], pos[1] // self.tile_size[1]]
            self.enter()
        elif self.check_in_sidebar(pos):
            tl = self.type_locations[0]
            self.flower_idx = (pos[1] - tl[1]) // self.tile_size[1]

    def step(self):
        self.board.step()
        shake = 0
        if self.round_started:
            if self.steps == self.steps_until_lava:
                self.audio_controller.start_erupt()
                shake = 1
                self.board.lava_outbreak(ROUNDS[self.round][0])
            self.steps += 1
            if not np.max(self.board.board == 1) and not np.max(self.board.threaten_tiles):
                self.round_started = False
                self.steps = 0
                self.seeds += self.seed_prod * np.sum(self.board.board == 3)
                self.board.delete_ice()
                self.round += 1
        # Check lose
        if not np.max(self.board.board == 3):
            self.lose = True
        return shake

    def set_tile(self, tile):
        self.board.set_tile(tile, self.hloc)

    def move_highlight(self, direction):
        self.hloc[0] = (self.hloc[0] + direction[0]) % self.board_size[0]
        self.hloc[1] = (self.hloc[1] + direction[1]) % self.board_size[1]

    def toggle_inv(self):
        self.flower_idx = (self.flower_idx + 1) % len(FLOWERS)

    def enter(self):
        if self.seeds < self.costs[self.flower_idx]:
            return
        c_type = self.board.board[self.hloc[0], self.hloc[1]]
        flower = FLOWERS[self.flower_idx]
        idx = TYPES.index(flower)
        if c_type == 1 or c_type == idx:
            return
        self.audio_controller.play_start(idx)
        self.seeds -= self.costs[self.flower_idx]
        self.set_tile(idx)

    def step_animate(self):
        self.animation_cnt = (self.animation_cnt + 1) % self.lcm

    def render(self, screen):
        # Render board
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                lay = ["Soil", None, None]
                type = TYPES[self.board.board[i, j]]
                if type in BACKGROUNDS:
                    lay[0] = type
                if self.board.threaten_tiles[i, j]:
                    lay[1] = "Threat"
                if type in TOP:
                    lay[2] = type

                all_dir = 0
                back = lay[0]
                for i2, cdir in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)][::-1]):
                    ni, nj = i + cdir[0], j + cdir[1]
                    if ni < 0 or ni >= self.board_size[0] or nj < 0 or nj >= self.board_size[1]:
                        continue
                    nt = TYPES[self.board.board[ni, nj]]
                    if nt not in BACKGROUNDS:
                        nt = "Soil"
                    if nt == back:
                        all_dir += 2**i2

                image_info = self.dir_dict[all_dir]
                tl_location = i * self.tile_size[0], j * self.tile_size[1]
                self.pygame_handler.render_tile(
                    screen, lay, image_info, tl_location, self.animation_cnt)

        # Render Sidebar
        for i, l in enumerate(self.type_locations):
            lay = ["Soil", None, None]
            lay[2] = FLOWERS[i]
            self.pygame_handler.render_tile(screen, lay, (0, 0), l, self.animation_cnt)

        tl_location = self.tile_size[0] * self.hloc[0], self.tile_size[1] * self.hloc[1]
        self.pygame_handler.render_highlight(screen, tl_location)

        # Render Seeds
        self.pygame_handler.render_text(screen, f"Seeds: {self.seeds}", self.seed_loc)
        self.pygame_handler.render_text(screen, f"Round: {self.round}",
                                        (self.seed_loc[0], self.seed_loc[1] + BORDER_WIDTH))
        for i, c in enumerate(self.costs):
            self.pygame_handler.render_text(screen, f"{c}", self.cost_locations[i])
        self.pygame_handler.render_text(
            screen, "Don't lose all your prized flowers!", self.bottom_loc)
        t = "r = restart" if self.lose else "s = Start Round    a = Speed Up"
        self.pygame_handler.render_text(
            screen, t, (self.bottom_loc[0], self.bottom_loc[1] + self.tile_size[1]//2))

        if self.lose:
            self.pygame_handler.render_title(screen, "You didn't keep it alive...", self.board_size_px)

        self.pygame_handler.render_select(screen, self.type_locations[self.flower_idx])
