"""
Lanes module for frogger

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _tiles: Row number of the lane being created
    # Invariant: _tiles is a non-zero int

    # Attribute _tile: The individual lane created
    # Invariant: _tile is a GTile

    # Attribute _jsondict = The current level's JSON dict
    # Invariant: _jsondict is a JSON file

    # Attribute _safe: A list of safe frogs that need to be created for each occupied exit
    # Invariant: _safe is an empty/non-empty list of GImages

    # Attribute _speed: The speed of the lane (and the objects in it)
    # Invariant: _speed is a non-zero int

    # Attribute _buffer: The offscreen buffer of the objects in the lane
    # Invariant: _buffer is a non-zero int

    # Attribute _objs: The list of objects in a lane
    # Invariant: _objs is either an empty list or non empty list of GImages

    # Attribute _singlelane: a dictionary of the lane with all the objects and positions
    # Invariant: _singlelane is a dictionary


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        '''Returns the row number of the lane created.'''
        return self._tile

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS

    def __init__(self,jsondict,tile,jsonhitbox):
        '''
        Initializes a lane with given tile and a JSON of level and JSON of objects

        The objects of the lane are put into a list and the list (if there are objects)
        are created with the lane. The objects are also assigned speeds.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file

        Paramter tile: The row number
        Precondition: tile is an integer
        '''
        self._jsondict = jsondict
        self._tiles = tile
        self._safe = []
        self._jsonhitbox = jsonhitbox
        self._objs = []
        self._singlelane = self._jsondict['lanes'][self._tiles]

        if 'speed' in self._singlelane:
            self._speed = self._singlelane['speed']
            self._buffer = self._jsondict['offscreen']

        if 'objects' in self._singlelane:
            objects = jsondict['lanes'][self._tiles]['objects']
            for i in range(len(objects)):
                type = objects[i]['type']
                object = GImage(x = objects[i]['position'] * GRID_SIZE + GRID_SIZE/2,
                 y = GRID_SIZE * tile + GRID_SIZE/2, source= objects[i]['type'] +'.png',
                 hitbox = self._jsonhitbox['images'][type]['hitbox'])
                if 'speed' in self._singlelane and self._jsondict['lanes'][tile]['speed'] <0:
                    object.angle = 180
                self._objs.append(object)

    def update(self,dt):
        for obj in self._objs:
            if 'speed' in self._singlelane:
                obj.x += self._speed * dt
                if obj.x < (-1 * self._buffer * GRID_SIZE):
                    d = (-1 * self._buffer * GRID_SIZE) - obj.x
                    obj.x = (self._jsondict['size'][0]*GRID_SIZE + self._buffer * GRID_SIZE) - d
                elif obj.x > (self._jsondict['size'][0]*GRID_SIZE) + self._buffer * GRID_SIZE:
                    d = self._jsondict['size'][0]*GRID_SIZE + self._buffer * GRID_SIZE - obj.x
                    obj.x = -1 * self._buffer * GRID_SIZE - d

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def draw(self,view):
        """
        Draws a lane, objects in the lane, and the safe frog is frog reaches exit
        """
        self._tile.draw(view)
        for obj in self._objs:
            obj.draw(view)
        for safefrog in self._safe:
            safefrog.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    def __init__(self,jsondict,tile,jsonhitbox):
        '''
        Initializes a Grass lane with given tile and a JSON of level and JSON of objects

        This calls the init of the Lane class to create the objects. This creates
        a GTile for a grass lane.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file

        Paramter tile: The row number
        Precondition: tile is an integer
        '''
        super().__init__(jsondict,tile,jsonhitbox)
        self._tile = GTile(left = 0, bottom = self._tiles*GRID_SIZE,
        width=self._jsondict['size'][0]*GRID_SIZE,height=GRID_SIZE, source= 'grass' +'.png')
    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    def __init__(self,jsondict,tile,jsonhitbox):
        '''
        Initializes a Road lane with given tile and a JSON of level and JSON of objects

        This calls the init of the Lane class to create the objects. This creates
        a GTile for a road lane.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file

        Paramter tile: The row number
        Precondition: tile is an integer
        '''
        super().__init__(jsondict,tile,jsonhitbox)
        self._tile = GTile(left = 0, bottom = self._tiles*GRID_SIZE,
         width=self._jsondict['size'][0]*GRID_SIZE,height=GRID_SIZE, source= 'road' +'.png')

    # DEFINE ANY NEW METHODS HERE
    def collideCar(self,frog):
        '''
        Returns if the frog is colliding with a car object in a lane.

        The function checks if the frog is colliding with any cars (objects) in
        the road lane. This returns True is frog is colliding with a car in the
        road and False if not.

        Paramater Frog: A frog object
        Precondition: Frog is a GImage
        '''
        for image in self._objs:
            if frog.collides(image):
                return True
        return False


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """

    def __init__(self,jsondict,tile,jsonhitbox):
        '''
        Initializes a Water lane with given tile and a JSON of level and JSON of objects

        This calls the init of the Lane class to create the objects. This creates
        a GTile for a water lane.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file

        Paramter tile: The row number
        Precondition: tile is an integer
        '''
        super().__init__(jsondict,tile,jsonhitbox)
        self._tile = GTile(left = 0, bottom = self._tiles*GRID_SIZE,
        width=self._jsondict['size'][0]*GRID_SIZE,height=GRID_SIZE, source= 'water' +'.png')

    def onLog(self,frog,width,animation,dt):
        '''Returns whether the frog is safe on a log or in the water

        This method returns 'lose life in water' if the frog moved offscreen
        on the log or is in the water, but returns 'safe' if on a log. This also
        moves the frog with the log if the frog is on the log'''
        for image in self._objs:
            if image.contains((frog.x,frog.y)) or animation is not None:
                frog.x += self._speed * dt
                if frog.x<0 or frog.x > width:
                    return 'lose life in water'
                else:
                    return 'safe'
        return 'lose life in water'


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    def __init__(self,jsondict,tile,jsonhitbox):
        '''
        Initializes a Hedge lane with given tile and a JSON of level and JSON of objects

        This calls the init of the Lane class to create the objects. This creates
        a GTile for a hedge lane.

        Parameter jsondictlvl: The JSON for level
        Precondition: jsondictlvl is a JSON file

        Paramter jsonhitbox: The JSON for objects and the hitboxes
        Precondition: jsonhitbox is a JSON file

        Paramter tile: The row number
        Precondition: tile is an integer
        '''
        super().__init__(jsondict,tile,jsonhitbox)
        self._tile = GTile(left = 0, bottom = self._tiles*GRID_SIZE,
        width=self._jsondict['size'][0]*GRID_SIZE,height=GRID_SIZE, source= 'hedge' +'.png')
        self._occupiedexits = []

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION

    # ANY ADDITIONAL METHODS
    def canCont(self,frog,direction):
        '''
        Returns if the frog is in an object and if it is, what type of objects

        This function goes through all objects (openings or exits)in Hedge and
        checks if the object contains a frog. If object contains frog, the function
        check if it is an exit and return 'is exit' if frog is in exit. If the object
        the frog is in is an opening, the function returns 'is opening'.
        It is also checked if the frog is trying to enter an occupied exit or if
        the frog is trying to move down into an exit. If this is attempted, function returns
        that it is in neither a exit or opening and is treated like a normal hedge.
        '''
        for image in self._objs:
            if image.contains((frog.x,(frog.y))):
                if image.source == 'exit.png':
                    if image in self._occupiedexits or direction == 'down':
                        return 'not in object'
                    else:
                        safefrog = GImage(x = image.x,y = image.y, source= 'safe.png')
                        self._safe.append(safefrog)
                        self._occupiedexits.append(image)
                        return 'is exit'
                elif image.source == 'open.png':
                    return 'is opening'
        return 'not in object'

    def getNumExits(self):
        '''
        Returns the number of exits that exits.

        This method uses an accumulator and goes through the number of exits in
        the water lane and adds the amount of exits to x. The x is then returned.
        '''
        x = 0
        for i in self._jsondict['lanes'][self._tiles]['objects']:
            if i['type'] == 'exit':
                x+=1
        return x

    def getNumOccupied(self):
        '''
        Returns the number of occupied exits in lane

        This checks the number of objects stored in the list (self._occupiedexits)
        of occupied exits and returns the number of occupies exits (the length
        of the list that stores exits)
        '''
        return len(self._occupiedexits)

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
