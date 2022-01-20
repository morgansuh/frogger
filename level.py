"""
Subcontroller module for frogger

This module contains the subcontroller to manage a single level in the frogger game.

The subcontroller Level manages the frog and all of the obstacles(defined in models.py).
This module contains the level class and all of the individual lanes.

"""
from game2d import *
from consts import *
from lanes  import *
from models import *


class Level(object):
    """
    This class controls a single level of frogger.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    frogger app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the frogger app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _lanes: The list of tiles(type of lane) of the Level
    # Invariant: _lanes is a list containing GTiles

    # Attribute _frog: The frog that the player uses to play the game
    # Invariant: _frog is a Frog object

    # Attribute _livesimg : A list of the frog images in the lives display
    # Invariant: _livesimg is a non empty/empty list of GImage

    # Attribute _livestext : The 'lives' text in the lives display
    # Invariant: _livestext is a GLabel

    # Atttribute _animator: Whether animating or not
    # Invariant: _aniamtor is None if nothing to animate or frog object of generator

    # Attribute _hitbox : json of the objects with the hitboxes
    # Invariant: _hitbox is a JSON dict

    # Attribute _input: Object of what the input is (up,down,left,or right)
    # Invariant: _input is a GInput

    # Attribute _width: Width of the level window
    # Invariant: _width is an int

    # Attribute _height: Height of the level window
    # Invariant: _height is an int

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLanes(self):
        '''returns the list of lanes (lane objects) in a level'''
        return self._lanes

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self,jsondictlvl,jsonhitbox):
        """
        Initializes a level with given level JSON and

        This level contains all lanes and objects. If frog is not None, a frog
        is created as well. There is also a display for the lives left created.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file
        """
        self._level = jsondictlvl
        self._hitbox = jsonhitbox

        self._lanes = []
        lanes = self._level['lanes']
        for tile in range(len(lanes)):
            if lanes[tile]['type'] == 'grass':
                lane = Grass(jsondictlvl,tile,jsonhitbox)
            elif lanes[tile]['type'] == 'water':
                lane = Water(jsondictlvl,tile,jsonhitbox)
            elif lanes[tile]['type'] == 'road':
                lane = Road(jsondictlvl,tile,jsonhitbox)
            elif lanes[tile]['type'] == 'hedge':
                lane = Hedge(jsondictlvl,tile,jsonhitbox)
            self._lanes.append(lane)

        self._animator = None
        self._frog = Frog(jsondictlvl)
        self._width = self._level['size'][0] * GRID_SIZE
        self._height= self._level['size'][1] * GRID_SIZE

        self._livesimg=[]
        for i in range(3):
            frog = GImage(x = (self._width- GRID_SIZE/2) - (i*GRID_SIZE),
            y =GRID_SIZE * len(lanes)+ GRID_SIZE/2, width = GRID_SIZE,
            height = GRID_SIZE,source=FROG_HEAD)
            self._livesimg.append(frog)
        self._livestext = GLabel(text = "lives:",font_name="AlloyInk.ttf",
        font_size =48,y = GRID_SIZE * len(lanes) + GRID_SIZE/2,
        linecolor = 'dark green')
        self._livestext.right = self._livesimg[2].left

    def update(self,input,dt):
        """
        Animates the frog slide.

        In this method the frog is moved based on input and it checks whether it can
        move (cannot move if going into a hedge or offscreen). The lanes are also updated
        and the method checks if the frog is in the water or collides with a car. If
        the frog does, the update also takes off a life from the display.

        Parameter dt: The arrow key pressed by user
        Precondition: input is 'up', 'down','left', or 'right'

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        self._input = input
        if self._animator is not None:          # We have something to animate
            try:
                self._animator.send(dt)
            except StopIteration:
                self._animator = None
        elif self._input.is_key_down('up'):
            return self._moveUp()
        elif self._input.is_key_down('down'):
            return self._moveDown()
        elif self._input.is_key_down('left'):
            self._moveLeft()
        elif self._input.is_key_down('right'):
            self._moveRight()

        for lane in self._lanes:
            lane.update(dt)
            if isinstance(lane,Water) and lane.getTile().collides(self._frog):
                if self._animator is None:
                    if lane.onLog(self._frog,
                    self._width,self._animator,dt) == 'lose life in water':
                        self._livesimg.pop(0)
                        self._frog = None
                        self._animator = None
                        if len(self._livesimg)>0:
                            return 'more lives left'
                        else:
                            return 'no lives left'

        if self._checkCarCollisions():
                return self._changeLives()

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Draws the lane,frog, and lives display into view.
        """
        for lane in self._lanes:
            lane.draw(view)
        if not self._frog == None:
            self._frog.draw(view)
        for frog in self._livesimg:
            frog.draw(view)
        self._livestext.draw(view)

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def reconstructFrog(self):
        '''
        Reconstructs a frog after state_paused

        The function recreates the Frog(object) after frog was assigned None.
        '''
        self._frog = Frog(self._level)

    def isWon(self,lane):
        '''
        Returns whether game is won or not.

        The function checks if the total number of exits is equal to the number
        of occupied exits. Returns True if the game is not yet won, but returns False
        if the game is won.

        Parameter lane: The Hedge lane
        Precondition: lane type is Hedge and is a GTile.
        '''
        return lane.getNumExits() != lane.getNumOccupied()

    def _moveUp(self):
        '''
        Moves the frog forward and checks for collisions with objects.

        The function moves the frog forward and changes the angle to north. It also
        checks if the frog is trying to go into a hedge or an exit. If the frog goes
        into an exit it returns "in exit". This function calls the coroutine to animate
        the frog moving up.
        '''
        self._frog.angle = FROG_NORTH
        if self._frog.y + GRID_SIZE <= self._height:
            self._frog.y += GRID_SIZE
            collide = self._checkCollide('up')
            self._frog.y -= GRID_SIZE
            if collide != 'cannot go':
                self._animator = self._frog.animateFrogVert('up')
                next(self._animator)
            if collide == 'is exit':
                self._frog = None
                return 'in exit'

    def _moveDown(self):
        '''
        Moves the frog downward and checks for collisions with objects.

        The function moves the frog downward and changes the angle to south. It also
        checks if the frog is trying to go into a hedge or an exit. If the frog goes
        into an exit it returns "in exit". This function calls the coroutine to animate
        the frog moving down.
        '''
        self._frog.angle = FROG_SOUTH
        if self._frog.y - GRID_SIZE >= 1:
            self._frog.y -= GRID_SIZE
            collide = self._checkCollide('down')
            if collide == 'cannot go':
                self._frog.y += GRID_SIZE
            else:
                self._frog.y += GRID_SIZE
                self._animator = self._frog.animateFrogVert('down')
                next(self._animator)
            if collide == 'is exit':
                self._frog = None
                return 'in exit'

    def _moveLeft(self):
        '''
        Moves the frog left and checks for collisions with objects.

        The function moves the frog forward and changes the angle to west. It also
        checks if the frog is trying to go into a hedge.
        This function calls the coroutine to animate the frog moving left.
        '''
        self._frog.angle = FROG_WEST
        if self._frog.x - GRID_SIZE >= 1:
            self._frog.x -= GRID_SIZE
            if self._checkCollide('left') == 'cannot go':
                self._frog.x += GRID_SIZE
            else:
                self._frog.x += GRID_SIZE
                self._animator = self._frog.animateFrogHor('left')
                next(self._animator)

    def _moveRight(self):
        '''
        Moves the frog right and checks for collisions with objects.

        The function moves the frog forward and changes the angle to east. It also
        checks if the frog is trying to go into a hedge.This function calls the
        coroutine to animate the frog moving up.
        '''
        self._frog.angle = FROG_EAST
        if self._frog.x + GRID_SIZE <= self._width:
            self._frog.x += GRID_SIZE
            if self._checkCollide('right') == 'cannot go':
                self._frog.x -= GRID_SIZE
            else:
                self._frog.x -= GRID_SIZE
                self._animator = self._frog.animateFrogHor('right')
                next(self._animator)

    def _changeLives(self):
        '''
        Changes lives display

        Function takes off a frog off of the list of frogs in the lives display.
        If there are no more frogs left after taking one off, the function
        returns "no lives left" to indicate all of the lives have been used. The
        function returns "more lives left" if the list still contaisn frog images
        (indicating not all lives were lost)
        '''
        if len(self._livesimg)>0:
            self._livesimg.pop(0)
        if len(self._livesimg)>0:
            return 'more lives left'
        else:
            return 'no lives left'

    def _checkCollide(self,direction):
         '''
         Checks for colliding with hedge and whether it is opening or exit in hedge

         The function checks each lane to see if frog is in a hedge lane.
         If in a hedge lane, function returns "is exit" if the frog is in an exit
         or 'cannot go' if it is going into an occupied exit or hedge, or 'is opening'
         if frog is entering a hedge opening.

         Parameter direction: The direction the frog is moving
         Precondition: direction is 'up,'down','left', or 'right'
         '''
         for lane in self._lanes:
             if isinstance(lane,Hedge) and lane.getTile().collides(self._frog):
                 if lane.canCont(self._frog,direction) == 'is exit':
                     return 'is exit'
                 if lane.canCont(self._frog,direction) == 'not in object':
                     return 'cannot go'
                 if lane.canCont(self._frog,direction) == 'is opening':
                     return 'is opening'

    def _checkCarCollisions(self):
         '''
         Check if frog is in any of the road lanes is colliding with a car

         The function loops through all the lanes and checks if the frog is in a
         Road lane. Then the fucntion checks if the frog collides with any car and
         if the frog is colliding with a car, frog is set to None and returns True.
         False is returned if car is not in Road or not colliding with a car.
         '''
         for lane in self._lanes:
             if self._frog is not None:
                 if isinstance(lane,Road) and lane.getTile().collides(self._frog):
                     if lane.collideCar(self._frog):
                         self._frog = None
                         return True
         return False
