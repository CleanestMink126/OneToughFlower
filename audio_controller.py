from constants import LAVA_THREAT, LAVA_ERUPT, DOGSONG, START_SOUNDS, DEATH_SOUNDS
import random
import math
import pygame


class AudioController:
    def __init__(self, channels):
        self.num_channels = channels
        pygame.mixer.set_num_channels(channels)

        self.curr_channel = 0

    def start_music(self):
        pygame.mixer.music.load(DOGSONG)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def start_threat(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(LAVA_THREAT))

    def start_erupt(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(LAVA_ERUPT))

    def play_start(self, type):
        if type in START_SOUNDS:
            c = self.curr_channel + 1
            list_sounds = START_SOUNDS[type]
            r = math.floor(random.random() * len(list_sounds))
            sound = pygame.mixer.Sound(list_sounds[r])
            sound.set_volume(1)
            pygame.mixer.Channel(c).play(pygame.mixer.Sound(list_sounds[r]))
            self.curr_channel = (self.curr_channel + 1) % (self.num_channels - 1)

    def play_death(self, type):
        if type in DEATH_SOUNDS:
            c = self.curr_channel + 1
            list_sounds = DEATH_SOUNDS[type]
            r = math.floor(random.random() * len(list_sounds))
            sound = pygame.mixer.Sound(list_sounds[r])
            sound.set_volume(0.4)
            pygame.mixer.Channel(c).play(sound)
            self.curr_channel = (self.curr_channel + 1) % (self.num_channels - 1)
