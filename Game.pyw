import os
import sys
import pygame
from pygame.locals import *
from constants import BOARD_SIZE, TOTAL_SIZE, BORDER_WIDTH
import random
# Our stuff
from board import Board
from controller import Controller
# -----------------
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


def input_to_board(controller,  keys, step_cnt):
    new_tiles = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_6: 5,
        pygame.K_7: 6,
        pygame.K_8: 7,
        pygame.K_9: 8
    }
    move_h = {
        pygame.K_LEFT: [-1, 0],
        pygame.K_RIGHT: [1, 0],
        pygame.K_UP: [0, -1],
        pygame.K_DOWN: [0, 1],
    }
    for k in new_tiles.keys():
        if keys[k]:
            controller.set_tile(new_tiles[k])
    for k in move_h.keys():
        if keys[k]:
            controller.move_highlight(move_h[k])

    if keys[pygame.K_a]:
        step_cnt = 0
    return step_cnt


def start_screen(screen, controller):
    c_screen = 0
    while 1:
        """detection of escape key to close program"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    c_screen += 1
                elif event.key == pygame.K_s:
                    c_screen += 10

        screen.fill((0, 0, 0))
        if c_screen == 0:
            controller.pygame_handler.render_text_center(
                screen, "One Tough Flower", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2))
        elif c_screen == 1:
            controller.pygame_handler.render_text_center(
                screen, "You are a farmer banished by your people.", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 - 2 * BORDER_WIDTH))
            controller.pygame_handler.render_text_center(
                screen, "Lost and without hope, you decide to travel", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 + 1 * BORDER_WIDTH))
            controller.pygame_handler.render_text_center(
                screen, " to the nearby volcano to sacrifice yourself", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 + BORDER_WIDTH * 3))
            controller.pygame_handler.render_text_center(
                screen, "to the corn gods.", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 + BORDER_WIDTH * 5))
        elif c_screen == 2:
            controller.pygame_handler.render_text_center(
                screen, "At the volcano, you discover a lone flower.", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2))
            controller.pygame_handler.render_text_center(
                screen, "You take this omen to mean you must build", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 + BORDER_WIDTH * 2))
            controller.pygame_handler.render_text_center(
                screen, "a beautiful garden on the sacred volcano.", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2 + BORDER_WIDTH * 4))
        elif c_screen == 3:
            controller.pygame_handler.render_text_center(
                screen, "This is your story.", (TOTAL_SIZE[0]/2, TOTAL_SIZE[1]/2))
        elif c_screen == 4:
            loc = (BORDER_WIDTH, BORDER_WIDTH)
            controller.pygame_handler.render_text_center(
                screen, "Types of flowers.", (TOTAL_SIZE[0]/2, loc[1]))
            loc = loc[0], loc[1] + BORDER_WIDTH + controller.tile_size[1]

            desc = [["These guys produce seeds, which let you plant flowers.", "But don't let them all die, or you'll fail!"],
                    ["These beefy boys will suck up lava.", "Use them to protect key points"],
                    ["These sneezer will blow away lava that lands on them", "in the direct they're facing."],
                    ["These guys are pretty weak,", "but they leave deadly blizzard in their wake."]]
            for i, type in enumerate(["MFlow", "BFlow", "DFlowd", "IFlow"]):
                lay = ["Soil", None, type]
                controller.pygame_handler.render_tile(screen, lay, (0, 0), loc, 0)
                for j, s in enumerate(desc[i]):
                    controller.pygame_handler.render_text(
                        screen, s, (loc[0] + controller.tile_size[0] + BORDER_WIDTH, loc[1] + j * BORDER_WIDTH))
                loc = loc[0], loc[1] + BORDER_WIDTH + controller.tile_size[1]
        else:
            break
        controller.pygame_handler.render_text_center(
            screen, "Press Enter to Continue", (TOTAL_SIZE[0]//2, (TOTAL_SIZE[0] * 1.5) // 2))

        pygame.display.flip()
        pygame.time.wait(33)


def loop():
    """this is where the game is set up and run"""
    pygame.init()
    controller = Controller()
    """screen size"""
    size = width, height = TOTAL_SIZE
    black = 0, 0, 0
    background = 30, 30, 30
    screen = pygame.display.set_mode(size)
    # ball = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 10, 0)
    center = [width/2, height/2]
    render_speed = 33
    animation_speed = 250
    animation_mult = animation_speed // render_speed
    animation_cnt = 0
    step_speed = 600
    step_mult = step_speed // render_speed
    step_cnt = 0
    top_shake = (20, 5)
    num_shake_frames = 35
    shake_list = [((i % 2) - random.random() * top_shake[0], (i % 2) - random.random() * top_shake[1])
                  for i in range(num_shake_frames)]
    shake_list += [(0, 0)]
    shake = 0
    controller.audio_controller.start_music()
    start_screen(screen, controller)
    """this is the main loop for the game"""

    while 1:
        """detection of escape key to close program"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    controller.enter()
                elif event.key == pygame.K_r:
                    controller = Controller()
                elif event.key == pygame.K_s:
                    shake += controller.start_round()
                elif event.key == pygame.K_i:
                    controller.toggle_inv()
            elif event.type == pygame.MOUSEBUTTONUP:   # handle MOUSEBUTTONUP
                pos = pygame.mouse.get_pos()
                controller.click(pos)
            elif event.type == pygame.MOUSEMOTION:
                controller.handle_mouse(pygame.mouse.get_pos())

        keys = pygame.key.get_pressed()  # checking pressed keys
        step_cnt = input_to_board(controller, keys, step_cnt)
        screen.fill(background)
        if not animation_cnt:
            controller.step_animate()
        if not step_cnt:
            shake += controller.step()
        if shake:
            controller.pygame_handler.shakex = shake_list[shake][0]
            controller.pygame_handler.shakey = shake_list[shake][1]
            shake += 1
            if shake == len(shake_list):
                shake = 0
        animation_cnt = (animation_cnt + 1) % animation_mult
        step_cnt = (step_cnt + 1) % step_mult
        controller.render(screen)
        pygame.display.flip()
        pygame.time.wait(render_speed)
    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    loop()
