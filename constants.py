import os
import sys


BOARD_SIZE = (10, 10)
BOARD_SIZE_PX = (600, 600)
BORDER_WIDTH = 20
TOTAL_SIZE = (750, 700)
FLOWERS = ["MFlow", "BFlow", "DFlowu", "DFlowr", "DFlowd", "DFlowl", "IFlow"]
TYPES = ["Soil", "Lava", "Rock"] + FLOWERS + ["Ice"]

d = [0, 2, 9, 5, 11, 15]

BACKGROUNDS = {
    "Soil": {d[0]: ["imgs/dirt/dirt1.png"], d[1]: ["imgs/dirt/dirt2.png"], d[2]: ["imgs/dirt/dirt3.png"], d[3]: ["imgs/dirt/dirt4.png"], d[4]: ["imgs/dirt/dirt5.png"], d[5]: ["imgs/dirt/dirt6.png"]},
    "Lava": {d[0]: ["imgs/lava/Lava1.png", "imgs/lava/Lava1p.png", "imgs/lava/Lava1.png", "imgs/lava/Lava1y.png"],
             d[1]: ["imgs/lava/Lava2.png", "imgs/lava/Lava2p.png", "imgs/lava/Lava2.png", "imgs/lava/Lava2y.png"],
             d[2]: ["imgs/lava/Lava3.png", "imgs/lava/Lava3p.png", "imgs/lava/Lava3.png", "imgs/lava/Lava3y.png"],
             d[3]: ["imgs/lava/Lava4.png", "imgs/lava/Lava4p.png", "imgs/lava/Lava4.png", "imgs/lava/Lava4y.png"],
             d[4]: ["imgs/lava/Lava5.png", "imgs/lava/Lava5p.png", "imgs/lava/Lava5.png", "imgs/lava/Lava5y.png"],
             d[5]: ["imgs/lava/Lava6.png", "imgs/lava/Lava6p.png", "imgs/lava/Lava6.png", "imgs/lava/Lava6y.png"]},
    "Rock": {d[0]: ["imgs/rock/rock1.png"], d[1]: ["imgs/rock/rock2.png"], d[2]: ["imgs/rock/rock3.png"], d[3]: ["imgs/rock/rock4.png"], d[4]: ["imgs/rock/rock5.png"], d[5]: ["imgs/rock/rock6.png"]},
    "Ice": {d[0]: ["imgs/ice/ice1.png"], d[1]: ["imgs/ice/ice2.png"], d[2]: ["imgs/ice/ice3.png"], d[3]: ["imgs/ice/ice4.png"], d[4]: ["imgs/ice/ice5.png"], d[5]: ["imgs/ice/ice6.png"]},
}

MIDDLE = {
    "Threat": ["imgs/threat1.png", "imgs/threat2.png", "imgs/threat3.png"],
}

TOP = {
    "MFlow": ["imgs/seed/mflow6.png", "imgs/seed/mflow7.png", "imgs/seed/mflow1.png", "imgs/seed/mflow2.png",
              "imgs/seed/mflow3.png", "imgs/seed/mflow4.png", "imgs/seed/mflow3.png", "imgs/seed/mflow5.png",
              "imgs/seed/mflow6.png", "imgs/seed/mflow7.png", "imgs/seed/mflow6.png", "imgs/seed/mflow7.png"],
    "BFlow": ["imgs/carrot/bflow1.png", "imgs/carrot/bflow2.png", "imgs/carrot/bflow1.png", "imgs/carrot/bflow3.png",
              "imgs/carrot/bflow1.png", "imgs/carrot/bflow2.png", "imgs/carrot/bflow1.png", "imgs/carrot/bflow3.png",
              "imgs/carrot/bflow4.png", "imgs/carrot/bflow5.png", "imgs/carrot/bflow4.png", "imgs/carrot/bflow3.png"],
    "IFlow": ["imgs/iflow/iflow1.png", "imgs/iflow/iflow2.png", "imgs/iflow/iflow1.png", "imgs/iflow/iflow3.png",
              "imgs/iflow/iflow1.png", "imgs/iflow/iflow2.png", "imgs/iflow/iflow1.png", "imgs/iflow/iflow3.png",
              "imgs/iflow/iflow1.png", "imgs/iflow/iflow4.png", "imgs/iflow/iflow5.png", "imgs/iflow/iflow4.png", ],
    "DFlowu": ["imgs/flowers/dflowu1.png", "imgs/flowers/dflowu2.png", "imgs/flowers/dflowu1.png", "imgs/flowers/dflowu3.png",
               "imgs/flowers/dflowu1.png", "imgs/flowers/dflowu2.png", "imgs/flowers/dflowu1.png", "imgs/flowers/dflowu3.png",
               "imgs/flowers/dflowu4.png", "imgs/flowers/dflowu2.png", "imgs/flowers/dflowu4.png", "imgs/flowers/dflowu3.png"],
    "DFlowr": ["imgs/flowers/dflowr1.png", "imgs/flowers/dflowr2.png", "imgs/flowers/dflowr1.png", "imgs/flowers/dflowr3.png",
               "imgs/flowers/dflowr4.png", "imgs/flowers/dflowr5.png", "imgs/flowers/dflowr4.png", "imgs/flowers/dflowr6.png",
               "imgs/flowers/dflowr7.png", "imgs/flowers/dflowr8.png", "imgs/flowers/dflowr7.png", "imgs/flowers/dflowr9.png"],
    "DFlowd": ["imgs/flowers/dflowd1.png", "imgs/flowers/dflowd2.png", "imgs/flowers/dflowd1.png", "imgs/flowers/dflowd3.png",
               "imgs/flowers/dflowd4.png", "imgs/flowers/dflowd5.png", "imgs/flowers/dflowd4.png", "imgs/flowers/dflowd6.png",
               "imgs/flowers/dflowd7.png", "imgs/flowers/dflowd8.png", "imgs/flowers/dflowd7.png", "imgs/flowers/dflowd9.png"],
    "DFlowl": ["imgs/flowers/dflowl1.png", "imgs/flowers/dflowl2.png", "imgs/flowers/dflowl1.png", "imgs/flowers/dflowl3.png",
               "imgs/flowers/dflowl4.png", "imgs/flowers/dflowl5.png", "imgs/flowers/dflowl4.png", "imgs/flowers/dflowl6.png",
               "imgs/flowers/dflowl7.png", "imgs/flowers/dflowl8.png", "imgs/flowers/dflowl7.png", "imgs/flowers/dflowl9.png"]
}

HIGHLIGHTER = "imgs/highlight.png"
SELECTOR = "imgs/selected.png"
LAVA_THREAT = "sounds/quake.wav"
LAVA_ERUPT = "sounds/explo.wav"
DOGSONG = "sounds/dogsong.mp3"
START_SOUNDS = {
    3: ["sounds/seed/g1.wav", "sounds/seed/g2.wav", "sounds/seed/g3.wav", "sounds/seed/g4.wav"],
    4: ["sounds/carrot/g1.wav", "sounds/carrot/g2.wav", "sounds/carrot/g3.wav", "sounds/carrot/g4.wav"],
    5: ["sounds/wind/g1.wav", "sounds/wind/g2.wav", "sounds/wind/g3.wav", "sounds/wind/g4.wav"],
    6: ["sounds/wind/g1.wav", "sounds/wind/g2.wav", "sounds/wind/g3.wav", "sounds/wind/g4.wav"],
    7: ["sounds/wind/g1.wav", "sounds/wind/g2.wav", "sounds/wind/g3.wav", "sounds/wind/g4.wav"],
    8: ["sounds/wind/g1.wav", "sounds/wind/g2.wav", "sounds/wind/g3.wav", "sounds/wind/g4.wav"],
    9: ["sounds/ice/g1.wav", "sounds/ice/g2.wav", "sounds/ice/g3.wav", "sounds/ice/g4.wav"]
}
DEATH_SOUNDS = {
    3: ["sounds/seed/b1.wav", "sounds/seed/b2.wav", "sounds/seed/b3.wav"],
    4: ["sounds/carrot/b1.wav", "sounds/carrot/b2.wav", "sounds/carrot/b3.wav"],
    5: ["sounds/wind/b1.wav", "sounds/wind/b2.wav", "sounds/wind/b3.wav"],
    6: ["sounds/wind/b1.wav", "sounds/wind/b2.wav", "sounds/wind/b3.wav"],
    7: ["sounds/wind/b1.wav", "sounds/wind/b2.wav", "sounds/wind/b3.wav"],
    8: ["sounds/wind/b1.wav", "sounds/wind/b2.wav", "sounds/wind/b3.wav"],
    9: ["sounds/ice/b1.wav", "sounds/ice/b2.wav", "sounds/ice/b3.wav"]
}
# Max Bad, Spot Precent
ROUNDS = [(100, 0.03), (50, 0.07), (100, 0.04), (300, 0.03), (100, 0.1), (2000, 0.02), (1000, 0.06),
          (1, 0.4), (5000, 0.01), (2000, 0.08), (1000, 0.01), (50, 0.3), (10000, 0.01), (300, 0.3)]
ROUNDS += [(10000*(1+i), 0.05 + i/100) for i in range(100)]
