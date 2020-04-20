from constants import BOARD_SIZE, BOARD_SIZE_PX, BORDER_WIDTH, TYPES, FLOWERS
import numpy as np
import random
from scipy import signal


filter = np.array(
    [[0.0207, 0.0292, 0.0207],
     [0.0292, 0.8, 0.0292],
     [0.0207, 0.0292, 0.0207]]
)

lava_rules = {
    5: (lambda x, l: x[1] > 0, lambda x: (x[0], x[1] - 1)),
    6: (lambda x, l: x[0] < l[0]-1, lambda x: (x[0] + 1, x[1])),
    7: (lambda x, l: x[1] < l[1]-1, lambda x: (x[0], x[1] + 1)),
    8: (lambda x, l: x[0] > 0, lambda x: (x[0] - 1, x[1])),
}


class Board:
    def __init__(self, audio_controller, board=None):
        self.board_size = BOARD_SIZE
        # Init board
        if board is None:
            board = np.zeros(self.board_size, np.int32)
        self.board = board
        self.tile_age = np.zeros(self.board_size, np.int32)
        self.tile_damage = np.zeros(self.board_size)
        self.lava_levels = np.zeros(self.board_size, np.int32)
        self.threaten_tiles = np.zeros(self.board_size, np.int32)
        self.blocker_health = 30
        self.ice_health = 50
        self.lava_decay = 0.99
        self.rock_max_age = 10
        self.lava_max_age = 7
        self.min_lava = 0.5
        self.audio_controller = audio_controller

    def set_tiles(self, condition, t):
        self.board = np.int32(np.where(condition, t[0], self.board))
        self.tile_age = np.int32(np.where(condition, t[1], self.tile_age))
        self.tile_damage = np.int32(np.where(condition, t[2], self.tile_damage))
        self.lava_levels = np.int32(np.where(condition, t[3], self.lava_levels))

    def set_tile(self, tile, loc):
        self.board[(loc[0], loc[1])] = tile
        self.tile_age[(loc[0], loc[1])] = 0
        self.tile_damage[(loc[0], loc[1])] = 0
        lev = 1000 if tile == 1 else 0
        self.lava_levels[(loc[0], loc[1])] = lev

    def threaten_lava_outbreak(self, chance):
        r = np.random.rand(self.board_size[0], self.board_size[1])
        condition = r < chance
        # p.int32(scale * r * (1.0/chance)
        self.threaten_tiles = condition

    def lava_outbreak(self, scale):
        r = np.random.rand(self.board_size[0], self.board_size[1])
        self.set_tiles(self.threaten_tiles, [1, 0, 0, r * scale])
        self.threaten_tiles = np.zeros(self.board_size, np.int32)

    def step(self):
        self.age_tiles()
        self.spread_lava()

    def delete_ice(self):
        self.set_tiles(self.board == 10, [0, 0, 0, 0])

    def check_boards(self, i, j):
        return i < 0 or j < 0 or i >= self.board_size[0] or j >= self.board_size[1]

    def spread_lava(self):
        lava_effect = signal.convolve2d(self.lava_levels, filter, mode="same")
        lava_effect = self.damage_tiles(lava_effect)
        # Find where lava should spread
        lava_thres = 1
        condition = (lava_effect > lava_thres) & np.logical_not(self.board == 1)
        deaths = np.where(condition & np.logical_not(self.board == 0) & np.logical_not(self.board == 2))
        for i, j in zip(deaths[0], deaths[1]):
            self.audio_controller.play_death(self.board[i, j])

            if self.board[i, j] == 9:
                # Ice flower
                for i1 in [-1, 0, 1]:
                    for j1 in [-1, 0, 1]:
                        if self.check_boards(i+i1, j+j1):
                            continue
                        self.set_tile(10, (i + i1, j + j1))
                        condition[i + i1, j + j1] = False
                        lava_effect[i + i1, j + j1] = 0

            # Set new lava tiles
        self.set_tiles(condition, [1, 0, 0, 0])
        self.lava_levels = lava_effect * self.lava_decay

    def push_lava(self, lava_effect, type):
        comp_f, shift_f = lava_rules[type]
        locs = np.where(self.board == type)
        condition = np.where(comp_f(locs, self.board_size))
        locs = locs[0][condition], locs[1][condition]
        new_locs = shift_f(locs)
        delta = np.copy(lava_effect[locs])
        return new_locs, locs, delta

    def damage_tiles(self, lava_effect):
        # Move tiles
        push_types = [5, 6, 7, 8]
        deltas = []
        for i in push_types:
            deltas.append(self.push_lava(lava_effect, i))

        for new_locs, locs, delta in deltas:
            lava_effect[new_locs] += delta
            lava_effect[locs] -= delta
        # Damage Defense Tiles
        condition = (self.board == 4) | (self.board == 10)
        self.tile_damage = np.where(condition, self.tile_damage + lava_effect, self.tile_damage)
        lava_effect = np.where(condition, 0, lava_effect)
        # Check if blocker is too damaged
        condition = (self.tile_damage > self.blocker_health) & (self.board == 4)
        for i in range(np.sum(condition)):
            self.audio_controller.play_death(4)
        self.set_tiles(condition, [0, 0, 0, 0])
        condition = (self.tile_damage > self.ice_health) & (self.board == 10)
        self.set_tiles(condition, [0, 0, 0, 0])
        return lava_effect

    def age_tiles(self):
        self.tile_age += 1
        # Age lava
        condition = (self.board == 1) & (self.tile_age > self.lava_max_age) & (self.lava_levels < self.min_lava)
        self.set_tiles(condition, [2, 0, 0, 0])
        # Age rock
        condition = (self.board == 2) & (self.tile_age > self.rock_max_age)
        self.set_tiles(condition, [0, 0, 0, 0])
