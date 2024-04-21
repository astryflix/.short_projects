#######################################
# 🚨 DEZE HELE CODE NIET BEWERKEN 🚨 #
#######################################

# Bévèro's world, v2: maze
# Author: Kevin van As
# School: Ashram College Alphen aan den Rijn
# Date:   31-01-2022
#
# Acknowledgements:
# This project was inspired by "Reeborg's World".
# Reeborg is unfortunately not available in Dutch, and therefore I created this code so my students can program in Dutch.
# Also, this provided me with more control over the levels to be more suited to my purposes.
#
# NEW in v2:
# - more maze levels (21 - 27), and minor changes to maze levels (18 - 20)
# - create your own maze (level 24 and "level 999")
# - 2 new player skins: ant and anteater
# - objects that can be placed and removed
# - levels that require reaching the end twice (25 - 27), allowing for a "seeker" player to retrace the steps of the first player.
# - the ability to show a route (i.e., a list of coordinate tuples)
#
# NEW in v3:
# - Random maze generator class + Randomised Kruskal Algorithm. Choose level 100 to execute it.
# - TODO: more random algorithms, including possibility to select a start/end position

import random

## Init pygame
import pygame

pygame.init()
clock = pygame.time.Clock()

#####
## Globl variables
EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270


#####
## World class
# 0 = wall
# 1 = path
# 2 = exit
###
class World():
    w = 50
    h = w

    error = None
    num_successes = 0

    # Custom_maze settings are only used in level 999.
    def __init__(self, level=0, custom_maze=None, custom_start_pos=None, custom_start_facing=SOUTH,
                 custom_cellsize=None):
        ## Init level
        # Defaults:
        self.player_start_pos = [0, 0]
        self.player_start_facing = SOUTH
        self.auto_win = False
        self.num_successes_required = 1
        # Level-specific:
        if level == 0:
            self.world = [
                [0, 0, 0],
                [0, 1, 0],
                [0, 2, 0],
                [0, 0, 0]
            ]
            self.player_start_pos = [1, 1]
            self.auto_win = True
        elif level == 1:
            self.world = [
                [0, 0, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 2, 0],
                [0, 0, 0]
            ]
            self.player_start_pos = [1, 1]
            self.auto_win = True
        elif level == 2:
            self.world = [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 2, 0],
                [0, 0, 0, 0, 0]
            ]
            self.player_start_pos = [1, 1]
            self.auto_win = True
        elif level == 3:
            self.world = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ]
            self.player_start_pos = [3, 1]
            self.auto_win = True
        elif level == 4:
            self.world = [
                [0, 0, 0, 0, 0],
                [0, 2, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ]
            self.player_start_pos = [3, 1]
            self.auto_win = True
        elif level == 5:
            self.world = [
                [2, 1, 1]
            ]
            self.player_start_pos = [0, 2]
            self.auto_win = True
        elif level == 6:  # hurde, without repeat
            # self.w = 30
            # self.h = self.w
            self.world = [
                [0, 1, 1, 1, 0],
                [1, 1, 0, 1, 2]
            ]
            self.player_start_pos = [1, 0]
            self.player_start_facing = EAST
            self.auto_win = True
        elif level == 7:  # hurde, repeat-5
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2]
            ]
            self.player_start_pos = [1, 0]
            self.player_start_facing = EAST
            self.auto_win = True
        elif level == 8:
            self.world = [
                [0, 0, 0],
                [0, 1, 0],
                [0, 2, 0],
                [0, 0, 0]
            ]
            self.player_start_pos = [1, 1]
        elif level == 9:
            self.world = [
                [1],
                [1],
                [1],
                [1],
                [1],
                [1]
            ]
            self.player_start_pos = [0, 0]
            self.world[random.randint(2, 4)][0] = 2
        elif level == 10:
            self.world = [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]
            ]
            self.player_start_pos = [3, 1]
            rnd = random.randint(0, 2)
            if rnd == 0:
                self.world[1][1] = 2
            elif rnd == 1:
                self.world[1][3] = 2
            else:
                self.world[3][3] = 2
        elif level == 11:  # hurdle, variable end point
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1]
            ]
            self.player_start_pos = [1, 0]
            self.player_start_facing = EAST
            # random ending point:
            self.world[1][random.choice(range(4, 21, 4))] = 2
        elif level == 12:
            self.world = [
                [0, 1, 1, 1],
                [0, 2, 0, 1],
                [0, 0, 0, 1],
                [1, 1, 1, 1]
            ]
            rnd = random.randint(0, 2)
            for i in range(rnd):
                self.world = self.world[:2] + [[0, 0, 0, 1]] + self.world[2:]
            self.player_start_pos = [len(self.world) - 1, 0]
        elif level == 13:  # stop at right time: straight, varying width
            self.world = [
                [2]
            ]
            for i in range(random.randint(2, 8)):  # random width
                self.world[0] = [1] + self.world[0]
            self.player_start_pos = [0, 0]
            self.player_start_facing = EAST
            self.auto_win = True
        elif level == 14:
            self.world = [
                [1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 1, 1],
                [1, 0, 1, 1, 1, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 2]
            ]
            self.player_start_pos = [2, random.randint(2, 3)]
        elif level == 15:  # hurde, variable distance
            self.w = 30
            self.h = self.w
            self.player_start_pos = [1, 0]
            self.player_start_facing = EAST
            worldLength = 99
            while worldLength > 25:  # set max length
                # print("repeat:", worldLength)
                self.world = [
                    [0, 1, 1, 1],
                    [1, 1, 0, 2]
                ]
                # Random number of hordes:
                rndNHordes = random.randint(2, 5)
                horde0 = [0, 1, 1, 1]
                horde1 = [1, 1, 0, 1]
                for i in range(rndNHordes):
                    # Random distance between this and next horde:
                    rndDistance = random.randint(0, 6)
                    for i in range(rndDistance):
                        self.world[0] = [0] + self.world[0]
                        self.world[1] = [1] + self.world[1]
                    # Add horde in front:
                    self.world[0] = horde0 + self.world[0]
                    self.world[1] = horde1 + self.world[1]
                worldLength = len(self.world[0])
        elif level == 16:
            self.world = [
                [0, 1, 0],
                [0, 1, 2]
            ]
            for i in range(random.randint(1, 4)):
                self.world.append([0, 1, 0])
            self.auto_win = True
            self.player_start_pos = [len(self.world) - 1, 1]
            self.player_start_facing = NORTH
        elif level == 17:  # hurde, variable height
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
            hor = 0
            while hor < len(self.world[0]) - 2:
                height = random.randint(1, 5)
                if height > 3:
                    height = random.randint(1, 5)  # minder kans voor hoog
                if hor + 3 >= len(self.world[0]) - 2:  # overwrite last horde: minimum height of 2
                    height = random.randint(2, 4)
                self.world[4][hor] = 1
                hor += 1
                for i in range(height):
                    self.world[4 - i][hor] = 1
                    self.world[4 - i][hor + 2] = 1
                self.world[4 - height + 1][hor + 1] = 1
                hor += 3
            self.world[-1][-1] = 2
            self.player_start_pos = [len(self.world) - 1, 0]
            self.player_start_facing = EAST
        elif level == 18:
            self.world = [
                [0, 1, 0, 1, 1, 0, 1, 0],
                [1, 1, 1, 1, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 0, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 1, 1]
            ]
            self.player_start_pos = [random.randint(0, 3), 6]
            rnd_end = random.randint(0, 3)
            if rnd_end == 0:
                self.world[2][3] = 2
            else:
                self.world[1][rnd_end] = 2
        elif level == 19:
            self.world = [
                [0, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 0, 0],
                [1, 0, 0, 1, 1, 0],
                [1, 0, 0, 0, 1, 1],
                [0, 2, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 1, 0]
            ]
            self.player_start_pos = [3, 0]
            self.player_start_facing = NORTH
        elif level == 20:  # maze, hug right wall to win
            self.world = [
                [1, 0, 0, 1, 0, 1, 2, 0],
                [1, 1, 1, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 1, 1, 1, 0],
                [0, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 0]
            ]
            self.player_start_pos = self.generate_random_pos()
        elif level == 21:  # same code as level 20 should work
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                [2, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
            ]
            self.player_start_pos = self.generate_random_pos()
        elif level == 22:  # level 21, but with a troublesome spawn
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                [2, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 1, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
            ]
            rnd = random.randint(0, 6)
            if rnd == 0:
                self.player_start_pos = [1, 4]
                self.player_start_facing = SOUTH
            elif rnd == 1:
                self.player_start_pos = [5, 1]
                self.player_start_facing = SOUTH
            elif rnd == 2:
                self.player_start_pos = [6, 4]
                self.player_start_facing = EAST
            elif rnd == 3:
                self.player_start_pos = [4, 9]
                self.player_start_facing = EAST
            elif rnd == 4:
                self.player_start_pos = [2, 5]
                self.player_start_facing = NORTH
            elif rnd == 5:
                self.player_start_pos = [3, 5]
                self.player_start_facing = WEST
            elif rnd == 6:
                self.player_start_pos = [7, 3]
                self.player_start_facing = WEST
            else:
                self.player_start_pos = [5, 9]
                self.player_start_facing = SOUTH
        elif level == 23:  # level 21, but with a troublesome spawn
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
                [2, 1, 0, 1, 0, 0, 1, 1, 0, 1],
                [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
            ]
            rnd = random.randint(0, 2)
            if rnd == 0:
                self.player_start_pos = [6, 1]
            elif rnd == 1:
                self.player_start_pos = [5, 1]
            else:
                self.player_start_pos = [5, 8]
            self.player_start_facing = random.randint(0, 3) * 90
        # elif level == 24:
        #   pass
        elif level == 25:  # maze with a loop: our code breaks down!!! ant solution
            self.w = 40
            self.h = self.w
            self.world = [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 2, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 0, 1],
                [0, 0, 1, 0, 0, 1, 1, 1],
            ]
            self.player_start_pos = [7, 2]
        elif level == 26:  # Like 25, but bigger. Just to test.
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
                [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
            ]
            self.player_start_pos = [2, 0]
            self.player_start_facing = EAST
        elif level == 27:  # like 25, but now requiring the second route-searching (anteater) phase to complete
            self.w = 40
            self.h = self.w
            self.world = [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 2, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 0, 1],
                [0, 0, 1, 0, 0, 1, 1, 1],
            ]
            self.player_start_pos = [7, 2]
            self.num_successes_required = 2
        elif level == 28:  # Like 27, but bigger. Just to test.
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
                [0, 1, 0, 1, 1, 1, 0, 2, 1, 0, 1, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
            ]
            self.player_start_pos = [2, 0]
            self.player_start_facing = EAST
            self.num_successes_required = 2
        elif level == 29:  # Like 27, but bigger. Just to test.
            self.w = 30
            self.h = self.w
            self.world = [
                [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
                [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
            ]
            self.player_start_pos = [2, 0]
            self.player_start_facing = EAST
            self.num_successes_required = 2
        elif level == 100:
            self.w = 15
            self.h = self.w
            mazesize = 25
            self.world = RandomizedKruskal(mazesize).generateMaze()
            endpoint = [-1, -1]
            while endpoint[0] != 0 and endpoint[0] != mazesize - 1 and endpoint[1] != 0 and endpoint[1] != mazesize - 1:
                endpoint = self.generate_random_pos()
            self.world[endpoint[0]][endpoint[1]] = 2
            self.player_start_pos = self.generate_random_pos()
        elif level == 101:
            self.w = 15
            self.h = self.w
            mazesize = 25
            numLoops = random.randint(5, 15)
            self.world = RandomizedKruskal(mazesize).generateMaze(numLoops=numLoops)
            endpoint = [-1, -1]
            while endpoint[0] != 0 and endpoint[0] != mazesize - 1 and endpoint[1] != 0 and endpoint[1] != mazesize - 1:
                endpoint = self.generate_random_pos()
            self.world[endpoint[0]][endpoint[1]] = 2
            self.player_start_pos = self.generate_random_pos()
        elif level == 999 or level == 24:
            self.change_maze(custom_maze, refresh=False)

            ## Sanity check on the other settings:
            # pos
            if custom_start_pos != None:
                if type(custom_start_pos) == list and len(custom_start_pos) == 2:
                    self.player_start_pos = custom_start_pos
                else:
                    raise ValueError("\nDit is geen mogelijke start positie: " + str(
                        custom_start_pos) + "! Ik heb een lijst met twee gehele getallen nodig. Bijvoorbeeld: rij 2 en kolom 4 is: [2,4]")
            else:
                print("Er wordt een willekeurige beginplek gekozen, omdat jij geen beginplek hebt ingesteld.")
                self.player_start_pos = self.generate_random_pos()
            # facing
            if custom_start_facing in [SOUTH, WEST, NORTH, EAST]:
                self.player_start_facing = custom_start_facing
            else:
                raise ValueError("\nJe gaf deze custom start facing:\n" + str(
                    custom_start_facing) + "\nmaar dat kan niet. Kies uit:\n zuid=" + str(SOUTH) + ", oost=" + str(
                    EAST) + ", noord=" + str(NORTH) + ", west=" + str(WEST))
        else:
            raise NotImplementedError(
                "\nLevel " + str(level) + " does not exist!\nLevel " + str(level) + " bestaat niet!")

        ## Is there a non-default cellsize set? Then overwrite the default:
        if custom_cellsize != None:
            self.resizeCells(custom_cellsize, refresh=False)

        ## Init pygame & background
        self.set_pygame_window()
        self.init_background()

    def set_pygame_window(self):
        ## Init pygame
        self.width = self.w * len(self.world[0])
        self.height = self.h * len(self.world)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def init_background(self):
        # print("init_background")
        ## Prepare background as a static image
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))

        # Draw tiles
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                # Do not draw walls
                if self.world[row][col] == 0:
                    continue
                pygame.draw.rect(
                    self.background,
                    (255, 255, 255),
                    pygame.Rect(
                        col * self.w + 2, row * self.h + 2,
                        self.w - 4, self.h - 4
                    )
                )

        # Draw paths between accessible tiles
        wpath = self.w // 2
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if not self.isAccessible([row, col]): continue
                if self.isAccessible([row + 1, col]):  # vertically downwards
                    pygame.draw.rect(
                        self.background,
                        (255, 255, 255),
                        pygame.Rect(
                            col * self.w + self.w // 2 - wpath // 2, (row + 1) * self.h - 2,
                            wpath, 4
                        )
                    )
                if self.isAccessible([row, col + 1]):  # horizontally right
                    pygame.draw.rect(
                        self.background,
                        (255, 255, 255),
                        pygame.Rect(
                            (col + 1) * self.w - 2, row * self.h + self.h // 2 - wpath // 2,
                            4, wpath
                        )
                    )

        # Draw exit
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.world[row][col] == 2:
                    pygame.draw.circle(
                        self.background,
                        (0, 50, 150),
                        (col * self.w + self.w // 2, row * self.h + self.h // 2),
                        self.w // 3
                    )
                    pygame.draw.circle(
                        self.background,
                        (0, 255, 0),
                        (col * self.w + self.w // 2, row * self.h + self.h // 2),
                        int(self.w * 0.27)
                    )

    def resizeCells(self, dim, refresh=True):
        try:
            self.w = int(dim[0])
            self.h = int(dim[1])
            if refresh:
                self.set_pygame_window()
                self.init_background()
        except:
            raise ValueError("Je probeerde de grootte van de vakjes te veranderen met " + str(
                dim) + ", maar ik verwacht een lijst met 2 getallen. Bijvoorbeeld: [30,30]")

    def change_maze(self, custom_maze, refresh=True):
        ## Sanity checks on the specified custom settings.
        if custom_maze != None:
            error_msg = ""
            if type(custom_maze) == list and type(custom_maze[0]) == list:
                lenrow0 = len(custom_maze[0])
                for i, row in enumerate(custom_maze):
                    if not type(row) == list:
                        error_msg = "Rij " + str(i + 1) + " is geen lijst. Maar dit moet wel!"
                        break
                    elif len(row) != lenrow0:
                        error_msg = "Rij " + str(
                            i + 1) + " is niet even lang als de eerste rij. Alle rijen moeten even lang zijn!"
                        break
                    else:
                        for tile in row:
                            if tile not in [0, 1, 2]:
                                error_msg = "Je mag alleen 0, 1 en 2 in de maze zetten, maar ik vond een: " + str(tile)
                                break
            else:
                error_msg = "Jouw doolhof is geen lijst met daarin lijsten, maar dat moet wel!"
            if error_msg != "":
                raise ValueError("\n\nJe gaf dit als custom maze:\n" + str(
                    custom_maze) + "\nMaar dit kan niet.\n\nERROR MESSAGE: " + str(
                    error_msg) + "\n\nIk heb een lijst nodig met daarin voor iedere rij een lijst met:\n0 = muur\n1 = pad\n2 = einde\nIedere rij moet even lang zijn.")
        else:
            raise NotImplementedError("\n\nLevel " + str(
                level) + " heeft een custom maze nodig, maar die heb jij nog niet toegevoegd toen je het level startte. Kijk de uitlegvideo. Daarin leg ik je precies uit wat je moet doen om dit level te kunnen spelen.")

        try:
            old_size = len(self.world)
            old_size = [old_size, len(self.world[0])]
        except:
            old_size = [0, 0]
        new_size = len(custom_maze)
        new_size = [new_size, len(custom_maze[0])]

        # No error, thus a valid maze was given:
        self.world = custom_maze

        ## Init pygame & background
        if refresh:
            if old_size != new_size:
                self.set_pygame_window()
            self.init_background()

    def draw(self):
        self.screen.blit(self.background, self.background.get_rect())

    def getcoords(self, pos, center=False):
        if center:
            return [pos[1] * self.w + self.w // 2, pos[0] * self.h + self.h // 2]
        else:
            return [pos[1] * self.w + 2, pos[0] * self.h + 2]

    # Checks whether the position (pos) is accessible.
    def isAccessible(self, pos):
        # Stand between tiles = not allowed:
        if int(pos[0]) != float(pos[0]) or int(pos[1]) != float(pos[1]):
            return False
        # Are we out of bounds? = not allowed
        if pos[0] < 0 or pos[0] >= len(self.world) or pos[1] < 0 or pos[1] >= len(self.world[0]):
            return False
        # Are we on an accessible (not-0) tile?
        return self.world[pos[0]][pos[1]] != 0

    # Generates a random position inside the world.
    # Use parameter "accessible = True" to enforce this position to be accessible.
    # Parameter "must_be_empty" makes sure that we cannot spawn on the exit (or any other future items I might add).
    def generate_random_pos(self, accessible=True, must_be_empty=True):
        # Check if there is an accessible tile AT ALL:
        if accessible:
            tot = 0
            for row in self.world:
                for item in row:
                    tot += item
            if tot == 0:  # inaccessible everywhere!!!
                raise ValueError(
                    "The current level does not have accessible tiles, thus a random accessible position cannot be generated.")

        # Generate random position:
        pos = [random.randint(0, len(self.world) - 1), random.randint(0, len(self.world[0]) - 1)]
        while (
                must_be_empty == False and (accessible and not self.isAccessible(pos))
        ) or (
                must_be_empty == True and (accessible and self.world[pos[0]][pos[1]] != 1)
        ):
            pos = [random.randint(0, len(self.world) - 1), random.randint(0, len(self.world[0]) - 1)]
        return pos

    # Set error to terminate the game after next draw
    def set_error(self, error=None):
        self.error = error

    def checkEndingReached(self, pos):
        return self.world[pos[0]][pos[1]] == 2

    # Determine if position (pos) equals the final tile
    def checkVictory(self, pos):
        if self.world[pos[0]][pos[1]] == 2:
            self.num_successes += 1
        return self.num_successes >= self.num_successes_required


class MazeGenerator():
    def __init__(self, size):
        # Sanity Check:
        if size % 2 == 0:
            raise ValueError(
                "Het doolhof moet een ONEVEN aantal vakjes groot zijn, maar jij gaf mij een even getal: " + str(
                    size) + ".")

        self.size = size

    def generateMaze(self, startCell=None, endCell=None):
        ## Build a wall-only maze:
        maze = []
        for i in range(self.size):
            rij = [0 for i in range(self.size)]
            maze.append(rij)
        ## Optionally add a start and end cell:
        if (type(startCell) == list or type(startCell) == tuple) and len(startCell) == 2:
            maze[startCell[0]][startCell[1]] = 1
        if (type(endCell) == list or type(endCell) == tuple) and len(endCell) == 2:
            maze[endCell[0]][endCell[1]] = 2
        return maze


class RandomizedKruskal(MazeGenerator):
    def __init__(self, size):
        super().__init__(size)

    def generateMaze(self, numLoops=0):
        # Start with an all-zeros maze:
        maze = super().generateMaze()

        ## Each walkable cell should be in its own set:
        sets = []
        for i in range(0, self.size, 2):
            for j in range(0, self.size, 2):
                sets.append(set(((i, j),)))
                maze[i][j] = 1

        ## Each wall should be added to a list:
        # (a wall has one even and one odd index)
        walls = []
        for i in range(0, self.size, 2):
            for j in range(0, self.size, 2):
                if i + 1 < self.size:
                    walls.append((i + 1, j))
                if j + 1 < self.size:
                    walls.append((i, j + 1))

        ## Algorithm: choose a random wall, and make it into a path iff it connects two disjoint sets.
        while len(sets) > 1 or numLoops > 0:
            # Choose a random wall:
            wall = random.choice(walls)
            # Is this a horizontal or a vertical connector?
            if wall[0] % 2 == 0:  # i = even, so horizontal
                nb1 = (wall[0], wall[1] - 1)
                nb2 = (wall[0], wall[1] + 1)
            else:  # i = odd, so vertical
                nb1 = (wall[0] - 1, wall[1])
                nb2 = (wall[0] + 1, wall[1])

            # Find the sets of the two neighbours
            for set0 in sets:
                if nb1 in set0:
                    set1 = set0
                if nb2 in set0:
                    set2 = set0

            # If the neighbours are from two distinct sets, then join the sets and convert the wall into a path:
            if set1 != set2:
                sets.remove(set1)
                sets.remove(set2)
                sets.append(set1.union(set2))
                maze[wall[0]][wall[1]] = 1
                # Done checking this wall:
                walls.remove(wall)
            elif numLoops > 0:  # otherwise create a loop, if we want one
                if random.random() < 0.05:  # with only 5% chance to prevent many small loops
                    numLoops -= 1
                    maze[wall[0]][wall[1]] = 1
            else:
                # Done checking this wall:
                walls.remove(wall)

        ## Done
        return maze


class Assets():
    ## Players
    SPRITE_BEAVER = "assets/sprites/player/beaver.png"
    SPRITE_BLOBFISH = "assets/sprites/player/blobfish.png"
    SPRITE_CHEETAH = "assets/sprites/player/cheetah.png"
    SPRITE_FOX = "assets/sprites/player/fox.png"
    SPRITE_OWL = "assets/sprites/player/owl.png"
    SPRITE_SQUID = "assets/sprites/player/squid.png"
    SPRITE_TURTLE = "assets/sprites/player/turtle.png"
    SPRITE_ANT = "assets/sprites/player/ant.png"
    SPRITE_ANTEATER = "assets/sprites/player/anteater.png"

    SPRITE_PLAYER_DEFAULT = SPRITE_BEAVER

    def random_player():
        rnd = random.randint(0, 8)
        if rnd == 0:
            return Assets.SPRITE_BEAVER
        elif rnd == 1:
            return Assets.SPRITE_BLOBFISH
        elif rnd == 2:
            return Assets.SPRITE_CHEETAH
        elif rnd == 3:
            return Assets.SPRITE_FOX
        elif rnd == 4:
            return Assets.SPRITE_OWL
        elif rnd == 5:
            return Assets.SPRITE_SQUID
        elif rnd == 6:
            return Assets.SPRITE_TURTLE
        elif rnd == 7:
            return Assets.SPRITE_ANT
        else:
            return Assets.SPRITE_ANTEATER

    ## Objects
    SPRITE_UNKNOWN = "assets/sprites/objects/unknown.png"
    SPRITE_ANTARROW = "assets/sprites/objects/arrow_pheromone.png"
    SPRITE_FLAG = "assets/sprites/objects/flag.png"

    SPRITE_OBJECT_DEFAULT = SPRITE_UNKNOWN


class Object():
    pos = [0, 0]  # what tile this object is on
    facing = SOUTH

    def __init__(self, world, pos=None, facing=SOUTH, sprite=None):
        self.world = world
        if pos != None:
            self.teleportTo(pos)
        if sprite != None:
            self.sprite = pygame.image.load(sprite)
        else:
            self.sprite = pygame.image.load(Assets.SPRITE_OBJECT_DEFAULT)
        self.rescale((int(world.w * 0.75), int(world.h * 0.75)))
        self.setFacing(facing)
        self.repositionSprite()

    def repositionSprite(self):
        self.sprite_rect.center = self.world.getcoords(self.pos, center=True)

    def teleportTo(self, newpos):
        if (type(newpos) == list or type(newpos) == tuple) and len(newpos) == 2:
            self.pos = newpos
        else:
            raise ValueError("Cannot teleport to " + str(
                newpos) + ", as that is not a valid position datatype. I require a list containing precisely two integers.")

    def rotate(self, dir=1):
        if dir >= 0:  # left (counter clockwise)
            self.facing = (self.facing + 90) % 360
            self.sprite = pygame.transform.rotate(self.sprite, 90)
        else:  # right (clockwise)
            self.facing = ((self.facing + 360) - 90) % 360
            self.sprite = pygame.transform.rotate(self.sprite, -90)
        # print("rotate:", "-->", self.facing)

    def setFacing(self, dir=SOUTH):
        # print("setFacing:", self.facing, "-->", dir)
        num_steps = int((dir - self.facing) / 90)
        if num_steps == 0: return
        pm = int(num_steps / abs(num_steps))
        for step in range(0, num_steps, pm):
            self.rotate(pm)
        # print(" --> results facing:", self.facing)

    def rescale(self, scale):
        self.sprite = pygame.transform.scale(self.sprite, scale)
        self.sprite_rect = self.sprite.get_rect()

    def draw(self):
        self.world.screen.blit(self.sprite, self.sprite_rect)


class Player(Object):

    def __init__(self, world, sprite=Assets.SPRITE_PLAYER_DEFAULT):
        super().__init__(world, world.player_start_pos, sprite=sprite)
        self.setFacing(world.player_start_facing)

    def move(self):
        will_error = False
        new_pos = self.get_after_move_pos()
        if self.world.isAccessible(new_pos):
            self.pos = new_pos
        else:
            self.pos = self.get_after_move_pos(0.5)
            self.world.set_error(
                "Je bent een muur in gelopen!\nDat betekent helaas dat jouw code het level niet oplost.\nProbeer het opnieuw!")
        self.repositionSprite()

    def get_after_move_pos(self, step=1):
        new_pos = [self.pos[0], self.pos[1]]
        if self.facing == SOUTH:
            new_pos[0] += step
        elif self.facing == NORTH:
            new_pos[0] -= step
        elif self.facing == EAST:
            new_pos[1] += step
        else:
            new_pos[1] -= step
        return new_pos


class Arrow(Object):
    def __init__(self, world, pos, facing=SOUTH):
        super().__init__(world, pos, facing, sprite=Assets.SPRITE_ANTARROW)


class Flag(Object):
    def __init__(self, world, pos, facing=SOUTH):
        super().__init__(world, pos, facing, sprite=Assets.SPRITE_FLAG)


## Global Functions to be used by "password_generator.py":
world = None
player = None
gamespeed = 2
game_running = False


def start(level=None, sprite=None, cellsize=None):
    global world, player, game_running

    if cellsize != None: cellsize = (cellsize, cellsize)

    world = World(level, custom_cellsize=cellsize) if level != None else World(custom_cellsize=cellsize)

    # Choose sprites based on active level
    if sprite == None:
        if level >= 100:  # random sprite
            player = Player(world, sprite=Assets.random_player())
        elif level >= 25:  # maze with pheromone
            player = Player(world, sprite=Assets.SPRITE_ANT)
        elif level >= 18:  # maze
            player = Player(world, sprite=Assets.SPRITE_BEAVER)
        elif level >= 16:  # rechts_van_mij & hurdle 4
            player = Player(world, sprite=Assets.SPRITE_OWL)
        elif level >= 12:  # muur_voor_mij & hurdle 3
            player = Player(world, sprite=Assets.SPRITE_CHEETAH)
        elif level >= 8:  # einde_bereikt & hurdle 2
            player = Player(world, sprite=Assets.SPRITE_FOX)
        elif level >= 6:  # hurdle 0-1
            player = Player(world, sprite=Assets.SPRITE_BLOBFISH)
        elif level >= 3:  # for-loop
            player = Player(world, sprite=Assets.SPRITE_TURTLE)
        else:  # stap en draai
            player = Player(world, sprite=Assets.SPRITE_SQUID)
    else:
        player = Player(world, sprite=sprite)

    # Small delay before start
    game_running = True
    refresh(wait=False)
    # print("Starting in 1 second...")
    clock.tick(1)


def clearAllThings():
    global player, players, objects
    player = None
    for i in range(len(players)):
        del players[0]
    for i in range(len(objects)):
        del objects[0]


# Start een eigen maze level MET een player.
def start_eigen_maze(maze, start_pos=None, start_facing=SOUTH, cellsize=None, sprite=None):
    global world, player, game_running, objects

    # First clear players/objects (if there were any from a previous level)
    clearAllThings()

    if cellsize != None: cellsize = (cellsize, cellsize)

    world = World(999, custom_maze=maze, custom_start_pos=start_pos, custom_start_facing=start_facing,
                  custom_cellsize=cellsize)

    if sprite == None:
        player = Player(world, sprite=Assets.random_player())
    else:
        player = Player(world, sprite=sprite)

    # Small delay before start
    game_running = True
    refresh(wait=False)
    # print("Starting in 1 second...")
    clock.tick(1)


# Start een eigen maze level ZONDER player. Alleen maze laten zien.
def show_eigen_maze(maze, cellsize):
    global world, game_running

    # First clear players/objects (if there were any from a previous level)
    clearAllThings()

    # Create
    world = World(999, custom_maze=maze, custom_start_pos=[0, 0], custom_cellsize=(cellsize, cellsize))

    # Show
    game_running = True
    refresh(wait=False)
    game_running = False


# Laat de eigen maze zien zonder pygame opnieuw te openen. Dit werkt alleen als "show_eigen_maze" of "start_eigen_maze" de eerste keer al is aangeroepen.
# Handig om een animatie te laten zien van een maze generator algorithm :)
def verander_maze(maze):
    global game_running

    # Edit
    world.change_maze(maze)

    # Show
    game_running = True
    refresh()
    game_running = False


def snelheid(v: object) -> object:
    global gamespeed
    gamespeed = v


players = []


def begin_spoorzoeker(sprite=None):
    global player, game_running
    players.append(
        player)  # zorgt ervoor dat de mier getekend blijft worden zodra de spoorzoeker de actieve speler wordt.
    if sprite == None:
        player = Player(world, sprite=Assets.SPRITE_ANTEATER)  # maze with pheromone
    else:
        player = Player(world, sprite=sprite)

    # Small delay before start
    game_running = True
    refresh(wait=False)
    clock.tick(1)


def muur_voor_mij():
    new_pos = player.get_after_move_pos()
    return not world.isAccessible(new_pos)


def muur_rechts_van_mij():
    player.rotate(-1)  # right
    new_pos = player.get_after_move_pos()
    player.rotate(1)  # back left
    return not world.isAccessible(new_pos)


def muur_links_van_mij():
    player.rotate(1)  # left
    new_pos = player.get_after_move_pos()
    player.rotate(-1)  # back right
    return not world.isAccessible(new_pos)


def stap():
    if not game_running:
        return
    player.move()
    refresh()


def draai_links():
    if not game_running:
        return
    player.rotate(1)
    refresh()


def draai_rechts():
    if not game_running:
        return
    player.rotate(-1)
    refresh()


objects = []


def plaats_hier(thing, facing=SOUTH):
    if type(thing) == type(Object) and issubclass(thing, Object):
        if is_ding_hier(thing):
            print("Waarschuwing: hier staat al een " + str(thing) + ", dus er wordt er NIET nog één geplaatst!")
        else:
            # print("plaats_hier: facing:", facing)
            new_thing = thing(world, player.pos, facing)
            objects.append(new_thing)
            refresh()  # redraw
    else:
        raise ValueError(
            "ERROR!!! Je probeerde een " + str(thing) + " te plaatsen, maar dit kan niet, want dat is geen Object!")


def is_ding_hier(thingType):
    return ding_hier(thingType) != None


def ding_hier(thingType):
    if type(thingType) == type(Object) and issubclass(thingType, Object):
        for obj in objects:
            # print("obj pos:", obj.pos, "; player.pos:", player.pos)
            if type(obj) == thingType and obj.pos == player.pos:
                # print("Returning object:", obj, obj.pos, obj.facing)
                return obj
        return None
    else:
        print("WAARSCHUWING!!! Je probeerde", thingType,
              "te vinden, maar dit kan niet, want dat is geen Object!\nDe code gaat wel gewoon door na deze waarschuwing.")


def verwijder_ding(thing):
    if thing in objects:
        objects.remove(thing)
        refresh()  # redraw
    else:
        print("WAARSCHUWING!!! Je probeerde", thing,
              "te verwijderen, maar dit kan niet, want dit is geen object of dit bestaat niet!\nDe code gaat wel gewoon door na deze waarschuwing.")


def einde_bereikt():
    global game_running
    if not game_running:
        return True

    if world.checkEndingReached(player.pos):
        if world.checkVictory(player.pos):
            game_running = False
            print('''
  ____  ____  ____      __    __  ____  ____   ______ 
 |    ||    ||    |    |  |__|  ||    ||    \ |      |
 |__  | |  | |__  |    |  |  |  | |  | |  _  ||      |
 __|  | |  | __|  |    |  |  |  | |  | |  |  ||_|  |_|
/  |  | |  |/  |  |    |  `  '  | |  | |  |  |  |  |  
\  `  | |  |\  `  |     \      /  |  | |  |  |  |  |  
 \____j|____|\____j      \_/\_/  |____||__|__|  |__| 
      ''')
        else:
            print('''
             _____   ____  _____   ___                      
            |     | /    T/ ___/  /  _]                     
            |   __jY  o  (   \_  /  [_                      
            |  l_  |     |\__  TY    _]                     
 __  __     |   _] |  _  |/  \ ||   [_      __  __          
|  T|  T    |  T   |  |  |\    ||     T    |  T|  T         
l__jl__j    l__j   l__j__j \___jl_____j    l__jl__j         

  _____ __ __    __    __    ___  _____ __ __   ___   _     
 / ___/|  T  T  /  ]  /  ]  /  _]/ ___/|  T  | /   \ | T    
(   \_ |  |  | /  /  /  /  /  [_(   \_ |  |  |Y     Y| |    
 \__  T|  |  |/  /  /  /  Y    _]\__  T|  |  ||  O  || l___ 
 /  \ ||  :  /   \_/   \_ |   [_ /  \ |l  :  !|     ||     T
 \    |l     \     \     ||     T\    | \   / l     !|     |
  \___j \__,_j\____j\____jl_____j \___j  \_/   \___/ l_____j

      ''')
            print("Gebruik dit commando om de volgende fase te beginnen:")
            print("begin_spoorzoeker()")
        # clock.tick(0.5)
        return True
    else:
        return False


def ik():
    return player


def kijk_naar(wie, richting):
    wie.setFacing(richting)
    refresh()  # redraw


def markeer(cells, objectType=Object):
    global player, players, objects, game_running
    if not (type(cells) == list or type(cells) == set):
        raise ValueError(
            "Ik heb een twee-dimensionale lijst als input nodig! Bijvoorbeeld: [ [0,0], [1,0], [2,0], [2,1] ].")

    # Clear players and objects
    clearAllThings()

    # Mark cells
    for i, tile in enumerate(cells):
        # Do we have a list of sets, with each set containing positions (list/tuple)?
        if type(tile) == set:
            print("set")
            for i, tile2 in enumerate(tile):
                # Sanity check
                if not (type(tile2) == list or type(tile2) == tuple) or len(tile2) != 2:
                    ValueError(
                        "Ik heb een twee-dimensionale lijst als input nodig! Bijvoorbeeld: [ [0,0], [1,0], [2,0], [2,1] ].")
                    # Create pointer
                objects.append(objectType(world, tile2))
        # Else: do we have a list of positions (list/tuple)?
        else:
            # Sanity check
            if not (type(tile) == list or type(tile) == tuple) or len(tile) != 2:
                ValueError(
                    "Ik heb een twee-dimensionale lijst als input nodig! Bijvoorbeeld: [ [0,0], [1,0], [2,0], [2,1] ].")
            # Create pointer
            objects.append(objectType(world, tile))

    # Refresh
    game_running = True
    refresh()
    game_running = False


def route_zien(route):
    markeer(route, objectType=Flag)


# def draai(dir=0):
#   if not game_running:
#     return

#   player.rotate(dir)
#   refresh()

## Ticks the draw & endgame check
def refresh(wait=True):
    global game_running
    if not game_running:
        return
    # Draw
    world.draw()
    for thing in objects:
        thing.draw()
    for p in players:
        p.draw()
    if player != None: player.draw()
    pygame.display.update()

    # Victory? / Defeat?
    if world.error != None:
        game_running = False
        print('''
  ____   ____  ___ ___    ___       ___   __ __    ___  ____  
 /    | /    ||   |   |  /  _]     /   \ |  |  |  /  _]|    \ 
|   __||  o  || _   _ | /  [_     |     ||  |  | /  [_ |  D  )
|  |  ||     ||  \_/  ||    _]    |  O  ||  |  ||    _]|    / 
|  |_ ||  _  ||   |   ||   [_     |     ||  :  ||   [_ |    \ 
|     ||  |  ||   |   ||     |    |     | \   / |     ||  .  \ 
|___,_||__|__||___|___||_____|     \___/   \_/  |_____||__|\_|
    ''')
        print(world.error)
    elif world.auto_win and einde_bereikt():
        pass
    # Wait
    if wait: clock.tick(gamespeed)
