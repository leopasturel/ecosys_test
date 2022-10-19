import os
import inspect

### Set up proper environment ###
# Get full actual file path
actual_file_path = inspect.getframeinfo(inspect.currentframe()).filename
# Get only filename of the actual file
actual_filename = os.path.basename(actual_file_path)
# Get parent folder path
path = os.path.dirname(os.path.abspath(actual_file_path))
# Set up new directory
os.chdir(path)

import pygame
from game_fct import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    