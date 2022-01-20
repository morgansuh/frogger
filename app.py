"""
Primary module for frogger

This module contains the main controller class for the frogger application.

"""
from consts import *
from game2d import *
from level import *
import colors_geom

from kivy.logger import Logger


# PRIMARY RULE: frogger can only access attributes in level.py via getters/setters
# frogger is NOT allowed to access anything in lanes.py or models.py.


class frogger(GameApp):
    """
    The primary controller class for the frogger application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Level object

        Method draw displays the Level object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Level.
    Level should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in a hidden
    attribute

    Attribute view: The game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView and is inherited from GameApp

    Attribute input: The user input, used to control the frog and change state
    Invariant: input is an instance of GInput and is inherited from GameApp
    """
    # HIDDEN ATTRIBUTES
    # Attribute _state: The current state of the game (taken from consts.py)
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _level: The subcontroller for a level, managing the frog and obstacles
    # Invariant: _level is a Level object or None if no level is currently active
    #
    # Attribute _title: The title of the game
    # Invariant: _title is a GLabel, or None if there is no title to display
    #
    # Attribute _text: A message to display to the player
    # Invariant: _text is a GLabel, or None if there is no message to display

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _win: A boolean that states True if game is won by filling all exits
    #Invariant: _win is a True or False expression

    #Attribute width: The width of the level window
    #Invarient: width is an integer in pixel size

    #Attribute height: The height of the level window
    #Invarient: height is an integer in pixel size
    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        creates both the title (in attribute _title) and a message (in attribute
        _text) saying that the user should press a key to play a game.
        """
        self._title = GLabel(text='frogger!',font_name="AlloyInk.ttf",
        font_size = 124, x = self.width/2,y = self.height/2,linecolor = 'green')
        self._text = GLabel(text = "press 's' to start",font_name="AlloyInk.ttf",
        font_size =64, x = self.width/2, y = self.height/2)
        self._level = None
        self._state = STATE_INACTIVE
        self.lastkey = 0
        self._win = False


    def update(self,dt):
        """
        Updates the game objects each frame.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Level. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Level object _level to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_LOADING, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays the title and a simple message on the screen. The application
        remains in this state so long as the player never presses a key.

        STATE_LOADING: This is the state that creates a new level and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame (the amount of time to load
        the data from the file) before switching to STATE_ACTIVE. One of the
        key things about this state is that it resizes the window to match the
        level file.

        STATE_ACTIVE: This is a session of normal gameplay. The player can
        move the frog towards the exit, and the game will move all obstacles
        (cars and logs) about the screen. All of this should be handled inside
        of class Level (NOT in this class).  Hence the Level class should have
        an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the frog after it was either killed
        or reached safety. The application switches to this state if the state
        was STATE_PAUSED in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to STATE_ACTIVE.
ss
        STATE_COMPLETE: The wave is over (all lives are lost or all frogs are safe),
        and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._text.top = self._title.bottom

        curr_keys = self.input.key_count
        if self._state == STATE_INACTIVE and curr_keys > 0 and (self.lastkey == 0 and self.input.is_key_down('s')):
            self._state = STATE_LOADING

        if self._state != STATE_INACTIVE:
            self._title = None

        if self._state == STATE_ACTIVE:
            self._stateActive(dt)

        if self._state == STATE_LOADING:
            self._stateLoading()

        if self._state == STATE_PAUSED:
            self._text = GLabel(text = "press 'c' to continue",font_name="AlloyInk.ttf",
            font_size = 64, x = self.width/2, y = self.height/2 - GRID_SIZE/2,linecolor = 'white',fillcolor = 'dark green',width = self.width, height = GRID_SIZE)
            if curr_keys > 0 and (self.lastkey == 0 and self.input.is_key_down('c')):
                self._state = STATE_CONTINUE
                self._level.reconstructFrog()

        if self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE

        if self._state == STATE_COMPLETE:
            self._text= GLabel(text = "you " + ('win' if self._win else 'lose'),font_name="AlloyInk.ttf",
            font_size = 64, x = self.width/2, y = self.height/2 - GRID_SIZE/2,linecolor = 'white', fillcolor = 'dark green',width = self.width, height = GRID_SIZE)

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw a
        GObject g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the cars, logs, and exits) are attributes
        in either Level or Lane. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        those two classes.  We suggest the latter.  See the example subcontroller.py
        from the lesson videos.
        """
        if self._state == STATE_INACTIVE:
            self._title.draw(self.view)
            self._text.draw(self.view)
        if self._state == STATE_LOADING:
            self._level.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._level.draw(self.view)
        if self._state == STATE_PAUSED:
            self._level.draw(self.view)
            self._text.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._level.draw(self.view)
            self._text.draw(self.view)
    # HELPER METHODS FOR THE STATES GO HERE

    def _stateActive(self,dt):
        '''
        Changes the state to the loading state

        This method reassigns the _text and _title attributes to None. Then loads in the
        level and objects JSON for the level window to be created and then changes
        state to STATE_INACTIVE.

        '''
        self._text = None
        x = self._level.update(self.input,dt)
        if x == 'more lives left' :
            self._state = STATE_PAUSED
        if x == 'in exit':
            self._win= True
            for lane in self._level.getLanes():
                if isinstance(lane,Hedge):
                    if self._level.isWon(lane):
                        self._win = False
                        break
            self._state = STATE_COMPLETE if self._win else STATE_PAUSED
        if x == 'no lives left':
            self._state = STATE_COMPLETE

    def _stateLoading(self):
        '''
        Changes the state to the loading state

        This method reassigns the _text and _title attributes to None. Then loads in the
        level and objects JSON for the level window to be created and then changes
        state to STATE_INACTIVE.

        '''
        self._text = None
        self._title = None
        defaultlvl = self.load_json(DEFAULT_LEVEL)
        hitbox = self.load_json('objects.json')
        self.width = defaultlvl['size'][0] * GRID_SIZE
        self.height = (defaultlvl['size'][1] + 1)* GRID_SIZE
        self._level = Level(defaultlvl,hitbox)
        self._state = STATE_ACTIVE
