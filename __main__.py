"""
The primary application script for frogger

This is the module with the application code. This module has to be in a folder
with the following files:

    app.py      (the primary controller class)
    level.py    (the subcontroller for a single game level)
    models.py   (the model classes)
    consts.py   (the application constants)

Tou should have the following subfolders:

    Fonts         (fonts to use for GLabel)
    Images        (image files to use in the game)
    JSON          (json files with the game data)

"""
from consts import *
from app import *

# Application code
if __name__ == '__main__':
    frogger(width=GAME_WIDTH,height=GAME_HEIGHT).run()
