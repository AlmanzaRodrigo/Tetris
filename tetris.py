# Rodrigo Almanza
# 2023-07-05
# final_project



from graphics import *
import random
import xbox_joystick as joy

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    """ 
    Block class:
    Implement a block for a tetris piece
    
    :attr x: type: int - specify the position on the tetris board in terms of the square grid
    :attr y: type: int - specify the position on the tetris board in terms of the square grid
    """

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)
        
        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        """
        The can_move function checks if the block can move dx squares in the x direction
        and dy squares in the y direction. It returns True if it can, and False otherwise.
        
        :param board: A Board object
        :param dx: Determine how many squares the block will move in the x direction
        :param dy: Determine how many squares the block will move in the y direction
        :return: A boolean value
        """
        return board.can_move(dx, dy)

    def move(self, dx, dy):
        """
        The move function moves the block dx squares in the x direction
        and dy squares in the y direction.
        
        :param dx: Move the block dx squares in the x direction
        :param dy: Move the block dy squares in the y direction
        :return: None
        """
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*self.BLOCK_SIZE, dy*self.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
    """ 
    Shape class:
    Base class for all the tetris shapes

    :attr blocks: type: list - the list of blocks making up the shape
    :attr rotation_dir: type: int - the current rotation direction of the shape
    :attr shift_rotation_dir: type: Boolean - whether or not the shape rotates
    """

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1

        # A boolean to indicate if a shape shifts rotation direction or not.
        # Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        """
        The get_blocks function returns a list of all the blocks in self.blocks.
                
        
        :return: A list of blocks
        """
        return self.blocks

    def draw(self, win):
        """
        The draw function draws each block in the blocks list.
        
        :param win: Canvas used to draw blocks
        :return: None
        """
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        """
        The move function moves the shape dx squares in the x direction
        and dy squares in the y direction, i.e. moves each of the blocks
        
        :param dx: Move the shape in the x direction
        :param dy: Move the shape in the y direction
        :return: None
        """
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        """
        The can_move function checks if the shape can move dx squares in the x direction
        and dy squares in the y direction, i.e. check if each of the blocks can move
        Returns True if all of them can, and False otherwise
        
        :param board: Board object to check if the shape is in a valid position
        :param dx: Move the shape dx squares in the x direction
        :param dy: Move the shape dy squares in the y direction
        :return: True if all the blocks can move and false otherwise
        """

        # Computes the new position of each block of the figure,
        # checks whether each block can move to the new position,
        # and returns a list of booleans.
        verified_pos_each_block = [block.can_move(board, block.x + dx, block.y + dy) for block in self.get_blocks()]
        
        # Checks if there is any block in the list that cannot be moved to the new position.
        if False in verified_pos_each_block:
            return False
        return True
    
    def get_rotation_dir(self):
        """
        The get_rotation_dir function returns the current rotation direction.
        
        :return: The current rotation direction
        """
        return self.rotation_dir

    def can_rotate(self, board):
        """
        The can_rotate function checks if the shape can be rotated.
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False. Otherwise all is good, return True
        
        :param board: Board object
        :return: A boolean value
        """
        # Obtains the rotation direction of the figure and the central block location
        # that will serve as the pivot point.
        dir = self.get_rotation_dir()
        center = self.blocks[1]

        # Calculates the new position of each block in the figure,
        # checks if each block can move to the new position,
        # and returns a list of booleans.
        verified_pos_each_block = []
        new_pos_each_block = []
        for block in self.blocks:
            x = center.x - dir*center.y + dir*block.y
            y = center.y + dir*center.x - dir*block.x
            verified_pos_each_block.append(block.can_move(board, x, y))
            new_pos_each_block.append((x - block.x, y - block.y))
            self.pos_each_block_rotated = new_pos_each_block
        
        # Checks if there is any block in the list that cannot
        # be moved to the new position.
        if False in verified_pos_each_block:
            return False
        else:
            return True

    def rotate(self, board):
        """
        The rotate function is responsible for rotating the shape.
        1. Get the rotation direction using the get_rotation_dir method
        2. Compute the position of each block after rotation
        3. Move the block to the new position

        :param board: Board object
        :return: None
        """

        if self.can_rotate:
            for i in range(len(self.blocks)):
                self.blocks[i].move(self.pos_each_block_rotated[i][0],
                                    self.pos_each_block_rotated[i][1])
 
        # Default behavior is that a piece will only shift
        # rotation direction after a successful rotation. This ensures that 
        # pieces which switch rotations definitely remain within their 
        # accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        
############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, '#2962FF')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, '#FFAE00')        
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, '#0AD2FF')        
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, '#FF0800')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, '#B4E600')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, '#FEFE00')
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, '#9500FF')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      


############################################################
# BOARD CLASS
############################################################

class Board():
    """ 
    Board class:
    It represents the Tetris board

    :attr width: type:int - width of the board in squares
    :attr height: type:int - height of the board in squares
    :attr canvas: type:CanvasFrame - where the pieces will be drawn
    :attr grid: type:Dictionary - keeps track of the current state of
                the board; stores the blocks for a given position
    """
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE + 3,
                                  self.height * Block.BLOCK_SIZE + 3)
        self.canvas.setBackground('gray12')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}
        
    def draw_shape(self, shape):
        """
        The draw_shape function draws the shape on the board if there is space for it
        and returns True, otherwise it returns False.
        
        :param shape: Shape object
        :return: Bool
        """
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        """
        1. check if it is ok to move to square x,y
        if the position is outside of the board boundaries, can't move there
        return False
        2. if there is already a block at that postion, can't move there
        return False
        3. otherwise return True        
        
        :param x: x position
        :param y: y position
        :return: Bool
        """
        # checks if position (x,y) is within the board
        if x >= self.width or y >= self.height:
            return False
        elif x < 0 or y < 0:
            return False
        
        # checks if there is no other block at position (x,y)
        if (x,y) in self.grid:
            return False
  
        return True

    def add_shape(self, shape):
        """
        The add_shape function adds a shape to the grid, i.e.
        adds each block to the grid using its (x, y) coordinates as a dictionary key
        
        :param shape: Shape object
        :return: None
        """
        blocks_list = shape.get_blocks()
        for block in blocks_list:
            self.grid[(block.x, block.y)] = block
        
        # Checks and removes any fully filled row.
        self.remove_complete_rows()

    def delete_row(self, y):
        """
        The delete_row function takes in a y value and removes all blocks in row y.
        Removes blocks from the grid and erases it from the screen.
        
        :param y: Determine which row to delete
        :return: None
        """
        listof_blocks = [item[1] for item in self.grid.items() if item[0][1] == y]
        listof_pos = [item[0] for item in self.grid.items() if item[0][1] == y]

        for block in listof_blocks: block.undraw()
        for pos in listof_pos: self.grid.pop(pos)
    
    def is_row_complete(self, y):
        """
        The is_row_complete function checks if a row is complete.
        It does this by checking the number of blocks in the grid that are in a given row,
        if there is one square that is not occupied, return False
        otherwise return True
        
        :param y: The number of the row to be checked
        :return: Bool
        """
        count = 0
        for pos in self.grid:
            if pos[1] == y:
                count += 1
        return count == self.width
    
    def move_down_rows(self, y_start):
        """
        for each row from y_start to the top
        for each column check if there is a block in the grid
        if there is, remove it from the grid
        and move the block object down on the screen
        and then place it back in the grid in the new position
        
        :param y_start: Specify the row from which start to move down all the blocks
        :return: A dictionary
        """
        # Computes all positions (x, y) that are above the row y_start.
        pos_above_y = [(x,y) for x in range(self.width) for y in range(y_start, -1, -1)]

        # Moves down one position each block in the self.grid list
        # that is above the row y_start
        for pos in pos_above_y:
            if pos in self.grid:
                self.grid[pos].move(0,1)
                self.grid[(pos[0],pos[1]+1)] = self.grid[pos]
                self.grid.pop(pos)

    def remove_complete_rows(self):
        """
        The remove_complete_rows function removes all the complete rows.
            1. for each row, y, 
            2. check if the row is complete
            if it is, delete the row move all rows down starting at row y - 1
        
        :return: None
        """
        for row in range(self.height):
            if self.is_row_complete(row):
                self.delete_row(row)
                self.move_down_rows(row)

    def game_over(self):
        """
        The game_over function displays a message in the center of the board
        that says "Game Over"; when there is no more space to place another piece.
        
        
        :return: None
        """
        block_size = Block.BLOCK_SIZE
        
        rectangle = Rectangle(Point(0 * block_size + 6, 7 * block_size),
                              Point(10 * block_size, 11* block_size))

        text = Text(Point(5 * block_size, 9 * block_size),
                         "No hay espacio para colocar otra pieza\nEl juego ha terminado")
        
        rectangle.setFill("#EDECED")
        rectangle.draw(self.canvas)
        text.draw(self.canvas)


############################################################
# TETRIS CLASS
############################################################


class Tetris():
    """
    Tetris class:
    Controls the game play
    
    :attr SHAPES: type: list (list of Shape classes)
    :attr DIRECTION: type: dictionary - converts string direction to (dx, dy)
    :attr BOARD_WIDTH: type:int - the width of the board
    :attr BOARD_HEIGHT: type:int - the height of the board
    :attr board: type:Board - the tetris board
    :attr win: type:Window - the window for the tetris game
    :attr delay: type:int - the speed in milliseconds for moving the shapes
    :attr current_shapes: type: Shape - the current moving shape on the board
    """
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1), 3:(-1, 0), 4:(1, 0), 2:(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    JOY_TURBO = 5   #  Values accepted within the range of 0 to 10.
    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.level_speed = 0.8
        self.list_pressed_btn = {}
        self.count = 50 # Enables the animation of block falling.

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)
        
        # Allows to capture input from an Xbox joystick
        self.joystick = self.joy_detect()

        # animate the shape!
        self.event_switcher()

    def create_new_shape(self):
        """
        The create_new_shape function creates a random new shape that is centered at the top of the board
        and returns the shape.
        
        :return: Shape object
        """
        # Randomly selects a tetromino from the self.SHAPES list.
        random_tetrominoe = self.SHAPES[random.randint(0,6)]
        
        # Returns the figure positioned centered at the top of the screen.
        return random_tetrominoe(Point(self.BOARD_WIDTH/2 , 0))
    
    def animate_shape(self):
        """
        The animate_shape function is responsible for moving the shape down at equal intervals
        specified by the delay attribute.
        
        
        :return: None
        """        
        self.do_move(self.DIRECTION['Down'])
    
    def do_move(self, direction):
        """
        Move the current shape in the direction specified by the parameter:
        First check if the shape can move. If it can, move it and return True
        Otherwise if the direction we tried to move was 'Down',
        1. add the current shape to the board
        2. remove the completed rows if any 
        3. create a new random shape and set current_shape attribute
        4. If the shape cannot be drawn on the board, display a game over message
        
        :param direction: type:string - Move the shape in a specific direction
        :return: Bool
        """
        dx, dy = direction

        if self.current_shape.can_move(self.board, dx, dy):
            self.current_shape.move(dx, dy)
            return True
        elif direction == (0, 1):
            # Adds all the blocks from current_shape to the board.
            self.board.add_shape(self.current_shape)

            # set the current shape to a random new shape
            self.current_shape = self.create_new_shape()

            # Draw the current_shape on the board (take a look at the
            # draw_shape method in the Board class)
            if not self.board.draw_shape(self.current_shape):
                self.board.game_over()

        return False

    def do_rotate(self):
        """
        The do_rotate function checks if the current_shape can be rotated and rotates it if it can.
        
        
        :return: None
        """
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)
    
    def key_pressed(self, event):
        """
        The key_pressed function is called when a key is pressed on the keyboard.
        If the user presses the arrow keys 'Left', 'Right' or 'Down', 
        the current_shape will move in the appropriate direction. If they press 
        the space bar, it will move down until it can no longer move and is added to 
        the board. If they press up, it should rotate.
        
        :param event: Get the key that was pressed
        :return: None
        """
        key = event.keysym
        if key in self.DIRECTION:
            self.do_move(self.DIRECTION[key])
        elif key == "Up":
            self.do_rotate()
        elif key == "space":
            can_move = True
            while can_move:
                can_move = self.do_move(self.DIRECTION["Down"])

    def joy_btn_pressed(self, event, value = 0):
        """
        The joy_btn_pressed function is called when a button on the joystick is pressed.
        The function checks if the button pressed corresponds to one of the directions in self.DIRECTION, and if so, calls do_move with that direction as an argument.
        If it's not a direction, then it checks for other buttons: 
            If event == 15 (the 'A' button), then call do_rotate() to rotate the piece clockwise 90 degrees; 
            If event == 13 (the 'B' button), then keep calling do_move(self.DIRECTION[2]) until can_move returns False
        
        :param event: Specifies which event the joystick is reporting.
        :param value: Determine the value asociate to the given event
        :return: None
        """
        
        if event in self.DIRECTION:
            self.do_move(self.DIRECTION[event])
        elif event == 15:
            self.do_rotate()
        elif event == 13:
            can_move = True
            while can_move:
                can_move = self.do_move(self.DIRECTION[2])

    def joy_capture(self, joy):
        """
        The joy_capture function allows to capture events from xbox joysticks.
        It requires as an argument an XInputJoystick object.
        When a button on the joystick is pressed, it executes the function on_button().
        When one of the axes of the joystick moves, it executes the function on_axis()
        
        :param joy: XInputjoystick object
        :return: None
        """

        @joy.event
        def on_button(button, pressed):
            if pressed:
                self.joy_btn_pressed(button)
                self.list_pressed_btn[button] = 0
            else:
                if button in self.list_pressed_btn:
                    self.list_pressed_btn.pop(button)

        @joy.event
        def on_axis(axis, value):
            self.joy_btn_pressed(axis, value)
        
        
        joy.dispatch_events()

        # Enables turbo action performed by the joystick when holding down a button.
        if self.list_pressed_btn != {}:
            print(self.list_pressed_btn)
            for btn in self.list_pressed_btn:
                if self.list_pressed_btn[btn] >= 10:
                    self.joy_btn_pressed(btn)
                    self.list_pressed_btn[btn] = 10 - self.JOY_TURBO
                else:
                    self.list_pressed_btn[btn] += 1

    def joy_detect(self):
        """
        The joy_detect function detects the connection of xbox joysticks connected and returns an XInputJoystick object
        if there is any
        
        :return: Joystick object or False
        """
        joysticks = joy.XInputJoystick.enumerate_devices()
        device_numbers = list(map(joy.attrgetter('device_number'), joysticks))

        if not joysticks:
            return False

        return joysticks[0]

    def event_switcher(self):
        """
        The event_switcher function is a subloop within the mainloop,
        it allows events to be triggered such as animate_shape() and 
        joy_capture()
        
        :return: None
        """
        if self.joystick != False:
            self.joy_capture(self.joystick)
        
        if self.count >= 100 * self.level_speed: 
            self.animate_shape()
            self.count = 0
        else: self.count += 1

        self.win.after(10, self.event_switcher)


################################################################
# Start the game
################################################################


win = Window("Tetris")
game = Tetris(win)
win.mainloop()

