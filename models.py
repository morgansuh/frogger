"""
Models module for frogger
"""
from consts import *
from game2d import *


class Frog(GImage):
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    pass

    def __init__(self,jsondict):
        '''
        Initializes a frog with jsondict of level

        A GImage of a frog is created and the positions of the frog
        are set based of the width and height of the level using jsondict

        Parameter jsondict: The JSON for level
        Precondition: jsondict is a JSON file
        '''
        super().__init__(source=FROG_IMAGE)
        self.x = (jsondict['start'][0]* GRID_SIZE)+ GRID_SIZE/2
        self.y = jsondict['start'][1] + GRID_SIZE/2
        self.angle = FROG_NORTH

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def animateFrogVert(self,direction):
        """
        Animates a slide of the image forward and back over FROG_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to rotate.
        Precondition: direction is a string and one of 'up' or 'down'.
        """
        svert = self.y
        if direction == 'up':
            fvert = svert+GRID_SIZE
        elif direction == 'down':
            fvert = svert-GRID_SIZE

        steps = (fvert-svert)/FROG_SPEED
        animating = True
        while animating:
            dt = (yield)

            amount = steps*dt
            self.y = self.y+amount

            if abs(self.y-svert) >= self.height:
                self.y = fvert
                animating = False

    def animateFrogHor(self,direction):
        """
        Animates a slide of the image left and right over FROG_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to rotate.
        Precondition: direction is a string and one of 'left' or 'right'.
        """
        svert = self.x
        if direction == 'left':
            fvert = svert-GRID_SIZE
        elif direction == 'right':
            fvert = svert+GRID_SIZE

        steps = (fvert-svert)/FROG_SPEED
        animating = True
        while animating:

            dt = (yield)

            amount = steps*dt
            self.x = self.x+amount

            if abs(self.x-svert) >= self.width:
                self.x = fvert
                animating = False
