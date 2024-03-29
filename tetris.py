"""This is a game of tetris developed by an absolute amateur. Thank you.
"""
import os
import random
import curses
import time


class Shape:
    """
    A class that represents a tetris shape. Classes of all of the main 7 tetris shapes are derived from this class.
    
    ...
        
    Attributes
    ----------
    direction : int
        This integer hold the information about how is the shape oriented. It can have values 0, 1, 2 or 3, but for
        some shapes the number of possible values is reduced thanks to symmetry. For example O_Block, which is a box
        of two by two squares looks the same no matter how it is rotated. The program is therefore simplified if we
        do not always consider all four possibilites.
    
    rotations : int
        Number of posible orientations a shape can have.
    
    position_x : int
        X coordinate of the bottom left corner of the shape.
    
    position_y : int
        Y coordinate of the bottome left corner of the shape.
    
    squares : list of lists of lists of int
        The first index chooses a direction. That is the first extraction by which we get a list of squares which make
        an shape in the chosen orietation. Each square is a list of two integers [y_coordiate, x_coordinate] relative 
        to the base point which is the bottom left corner of the shape These lists do not change during the game.
    """

    def __init__(self):
        """This constructor initializes a few parameters that all of the shapes use.
        
        ...
        Parameters
        ----------
        none
        """
        self.direction = 0  # Initialize direction attribute 
        self.rotations = 1  # Initialize rotations attribute
        self.squares = []  # Initialize squares
        self.position_x = 4  # Initialize position x so that it starts in the middle
        self.position_y = 0  # Initialize position y so that it starts outside of the visible field
        
    def move_down(self):
        """Function that represnts a 'down' movement of the shape.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_y += 1
        
    def move_left(self):
        """Function that represnts a'left' movement of the shape.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_x -= 1
        
    def move_right(self):
        """Function that represnts a 'right' movement of the shape.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_x += 1

    def get_squares(self,rotated=False):
        """'The getter' of list of the squares that represent the shape of the shape.
        
        Parameters
        ----------
        rotated : bool, optional 
            When True, the returned list of squares is not of the current orientation but of a clock-wisely rotated one.
            
        Returns
        -------
        list of squares that represent the shape. If rotated is not stated or is False, the returned shape
        corresponds to the current orientation of the shape represented by the attribute 'self.direction'.
        """
        if not rotated:
            return self.squares[self.direction]
        return self.squares[self.direction-self.rotations+1]
    
    def rotate(self):
        """
        A function representing a rotation of a particular shape based on how many different orientations it has.
        We only use a clock-wise rotation which is represented by incrementing a variable self.direction by one modulo 
        number of possible orientations stored in variable self.rotations.
        ...
        Arguments
        ---------
        none
        
        Returns
        -------
        nothing
        """
        if self.rotations == 1:
            return
        
        if self.rotations == 2:
            if not self.direction:
                self.direction = 1
                return
            self.direction = 0
            return
        
        if self.rotations == 4:
            self.direction = (self.direction+1)%4
            return
    
class O_Block(Shape):
    """
    Shape that is a two by two box - O. It has only one orientation thanks to rotations symmetry.
    The block looks like this:
                        self.direction == 0 : |#|#|
                                              |#|#|      
    """
    def __init__(self):
        super(O_Block, self).__init__()
        self.squares.append([[0,0],[0,1],[1,0],[1,1]])
        

class I_Block(Shape):
    """
    Shape that is one four by one line. It has two orientations (directions).
    The block looks like this:
                        self.direction == 0 : |#|
                                              |#|
                                              |#|
                                              |#|
                                             
                        self.direction == 1 : |#|#|#|#|
    """
    def __init__(self):
        super(I_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[0,0],[1,0],[2,0],[3,0]])  
        self.squares.append([[0,0],[0,1],[0,2],[0,3]])


class T_Block(Shape):
    """
    This block has four orientations.
    The block looks like this:
                        self.direction == 0 :    |#|
                                               |#|#|#|
                                               
                        self.direction == 1 :  |#|
                                               |#|#|
                                               |#|
                                                   
                        self.direction == 3 :   |#|#|#|
                                                  |#|

                        self.direction == 4 :    |#|
                                               |#|#|
                                                 |#|
    """
    def __init__(self):
        super(T_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,0], [0,1], [0,2], [1,1]])
        self.squares.append([[0,0], [1,0], [1,1], [2,0]])
        self.squares.append([[1,0], [0,1], [1,1], [1,2]])
        self.squares.append([[0,1], [1,0], [1,1], [2,1]])

    
class Z_Block(Shape):
    """
    The block in the shape of the letter z.
    The block looks like this:
                        self.direction == 0: |#|#|
                                               |#|#|
                                             
                        self.direction == 1:     |#|
                                               |#|#|
                                               |#|
    """ 
    def __init__(self):
        super(Z_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[1,0], [0,1], [1,1], [0,2]])
        self.squares.append([[0,0], [1,0], [1,1], [2,1]])
    
    
class S_Block(Shape):
    """
    The block in the shape of the letter s.
    The block looks like this:
                        self.direction == 0:   |#|#|
                                             |#|#|
                                             
                        self.direction == 1:   |#|
                                               |#|#|
                                                 |#|
    """ 
    def __init__(self):
        super(S_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[0,0], [0,1], [1,1], [1,2]])
        self.squares.append([[0,1], [1,0], [1,1], [2,0]])
    
    
class L_Block(Shape):
    """
    The block in the shape of the letter L.
    The block looks like this:
                        self.direction == 0:  |#|
                                              |#|
                                              |#|#|
                                             
                        self.direction == 1:  |#|#|#|
                                              |#|

                        self.direction == 2:  |#|#|
                                                |#|
                                                |#|
                                             
                        self.direction == 3:      |#|
                                              |#|#|#|
    """ 
    def __init__(self):
        super(L_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,0], [0,1], [1,0], [2,0]])
        self.squares.append([[0,0], [1,0], [1,1], [1,2]])
        self.squares.append([[0,1], [1,1], [2,1], [2,0]])
        self.squares.append([[0,0], [0,1], [0,2], [1,2]])
    
    
class J_Block(Shape):
    """
    The block in the shape of the letter J.
    The block looks like this:
                        self.direction == 0:    |#|
                                                |#|
                                              |#|#|
                                             
                        self.direction == 1:  |#|
                                              |#|#|#|

                        self.direction == 2:  |#|#|
                                              |#|
                                              |#|
                                             
                        self.direction == 3:  |#|#|#|
                                                  |#|
    """ 
    def __init__(self):
        super(J_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,1], [1,1], [2,1], [0,0]])
        self.squares.append([[0,0], [0,1], [0,2], [1,0]])
        self.squares.append([[0,0], [2,1], [1,0], [2,0]])
        self.squares.append([[0,2], [1,0], [1,1], [1,2]])
    

# TODO: maybe flash a row that is full
# TODO: add docummentation to the classes - in progress
# TODO: add a different GUI - for example a TKinter

class TetrisGUI():
    def draw_game(self):
        return
    def draw_main_pad(self):
        return
    def draw_score_pad(self):
        return
    def draw_new_pad(self):
        return
    
class CursesTetrisGUI(TetrisGUI):
    """
    Console tetris GUI class derived from TetrisGUI. 
    """
    def __init__(self, stdscr):
        """
        Constructor of console GUI class.
        ...
        Arguements
        ----------
        stdscr : curses screen
        """
        self.stdscr = stdscr
        self.left_offset = 4
        self.upper_offset = 2
        self.main_pad = curses.newpad(26, 21)
        self.score_pad = curses.newpad(5, 9)
        self.next_pad = curses.newpad(8,16)

    def draw_game(self,next_object):
        self.stdscr.clear()
        # Draw tetris box
        for i in range(21):
            self.stdscr.addstr(i+self.upper_offset, self.left_offset,"|")
            self.stdscr.addstr(i+self.upper_offset, 20+self.left_offset,"|")
            
        for i in range(19):   
            self.stdscr.addstr(20+self.upper_offset, i+self.left_offset+1,"-")
        
        # Draw next pad
        self.stdscr.addstr(self.upper_offset, 29,"----------------")
        self.stdscr.addstr(self.upper_offset+8, 29,"----------------")
        for i in range(9):
            self.stdscr.addstr(self.upper_offset+i, 29, "|")
            self.stdscr.addstr(self.upper_offset+i, 45, "|")

        self.stdscr.refresh()
        self.draw_next_pad(next_object)
        self.draw_score_pad(0)
        
    def draw_taken_squares(self, free_squares):
        for i in range(1,21):
            for j in range(10):
                if [i,j] in free_squares: 
                    self.main_pad.addstr(i+4,j*2+1, ". ")
                    continue
                self.main_pad.addstr(i+4,j*2,"|@|")

    def draw_object(self,obj):
        for square in obj.get_squares():
            row = obj.position_y-square[0]+4
            col = obj.position_x+square[1]
            self.main_pad.addstr(row,col*2,"|#|")      

        self.main_pad.refresh(5, 1, self.upper_offset, self.left_offset+1 ,20+self.upper_offset-1 ,19+self.left_offset)

    def draw_main_pad(self, free_squares, current_object):
        self.main_pad.clear()
        self.draw_taken_squares(free_squares)
        self.draw_object(current_object) 
  
    def draw_score_pad(self, score):
        self.score_pad.addstr(0,1," SCORE")
        self.score_pad.addstr(1,0,"---------")
        self.score_pad.addstr(2,0,"| {0:05d} |".format(score))
        self.score_pad.addstr(3,0,"---------")
        self.score_pad.refresh(0,0,15,30,20,38)

    def draw_next_pad(self, obj):
        self.next_pad.clear()
        for square in obj.get_squares():
            row = -square[0]+4
            col = 2+square[1]
            self.next_pad.addstr(row,col*2,"|#|")      
        self.next_pad.refresh(0,0,3,31,9,43)


class Game():
    def __init__(self, tetris_gui):
        self.tetris_gui = tetris_gui
        self.score = 0
        self._ended = False
        self.current_object = None
        self.next_object = self.generate_object()
        self.tetris_gui.draw_game(self.next_object)
        self.current_object = self.generate_object()
        self.tetris_gui.draw_object(self.current_object)
        self.free_squares = [[i,j] for j in range(10) for i in range(-5,21)]
    
    def reset(self):
        self.__init__(self.tetris_gui)
    
    @property
    def ended(self):
        return self._ended
    
    def update_next_object(self):
        self.next_object = self.generate_object()
        self.tetris_gui.draw_next_pad(self.next_object)
        
    def update_score(self, erased_lines):
        if erased_lines == 1:
            self.score += 1
        elif erased_lines == 2:
            self.score += 4
        elif erased_lines == 3:
            self.score += 16
        elif erased_lines == 4:
            self.score += 64

        self.tetris_gui.draw_score_pad(self.score)
        
    def can_rotate(self,moved_left=0):
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.get_squares(rotated=True):
            if not [-square[0]+y, square[1]+x-moved_left] in self.free_squares:
                return False
        return True
    
    def can_move_down(self):
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.get_squares():
            if not [-square[0]+y+1,square[1]+x] in self.free_squares:
                return False
        return True

    def can_move_right(self):
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.get_squares():
            if not [-square[0]+y,square[1]+x+1] in self.free_squares:
                return False
        return True
        
    def can_move_left(self):
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.get_squares():
            if not [-square[0]+y,square[1]-1+x] in self.free_squares:
                return False
        return True

    def rotate(self):
        if self.can_rotate(): 
            self.current_object.rotate()
            return     
        if self.can_rotate(moved_left=1):
            self.current_object.move_left()
            self.current_object.rotate()
            return
        if self.can_rotate(moved_left=2):
            self.current_object.move_left()
            self.current_object.move_left()
            self.current_object.rotate()
            return
        if self.can_rotate(moved_left=3):
            self.current_object.move_left()
            self.current_object.move_left()
            self.current_object.move_left()
            self.current_object.rotate()
            return

    def move_down(self):
        if not self.can_move_down():
            return
        self.current_object.move_down()
    
    def move_right(self):
        if not self.can_move_right():
            return
        self.current_object.move_right()
    
    def move_left(self):
        if not self.can_move_left():
            return
        self.current_object.move_left()

    def generate_object(self):
        gen = random.randint(0, 6)
        if gen == 0:
            return O_Block()
        if gen == 1:
            return I_Block()
        if gen == 2:
            return T_Block()
        if gen == 3:
            return Z_Block()
        if gen == 4:
            return S_Block()
        if gen == 5:
            return L_Block()
        if gen == 6:
            return J_Block()


    def place_object(self):
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.get_squares():
            self.free_squares.remove([-square[0]+y,square[1]+x])
        self.current_object = self.next_object
            
    def get_full_lines(self):
        lines = []
        for i in range(20,0,-1):
            line = True
            for j in range(10):
                if [i,j] in self.free_squares: 
                    line = False
                    break
            if line: 
                lines.append(i)
        return lines       

    def remove_and_move_lines(self,lines):
        full_lines = sorted(lines)
        for line_index in range(21):
            if not line_index in full_lines: continue
            for sq in self.free_squares:
                if sq[0]< line_index:
                    sq[0] += 1
            for i in range(10):
                self.free_squares.append([-5,i])

    def check_lose(self):
        for i in range(10):
            if [0,i] not in self.free_squares: return True    
        return False
    
    def progress(self):
        if not self.can_move_down():
            self.place_object()
            if self.check_lose():
                self._ended = True
                return
            self.update_next_object()
            full_lines = self.get_full_lines()
            if full_lines:
                self.remove_and_move_lines(full_lines)
                self.update_score(len(full_lines))
            return        
        self.current_object.move_down()
        self.update_main_pad()
    
    def update_main_pad(self):
        self.tetris_gui.draw_main_pad(self.free_squares, self.current_object)
        
    def user_input(self, key):
        if key == curses.KEY_RIGHT:
            self.move_right()
        elif key == curses.KEY_LEFT:
            self.move_left()
        elif key == curses.KEY_UP:
            self.rotate()
        elif key == curses.KEY_DOWN:
            self.move_down()
        curses.flushinp()
            
        self.update_main_pad()


def curses_main(stdscr):
    stdscr.clear()
    stdscr.nodelay(1)
    tetris_gui = CursesTetrisGUI(stdscr)
    game = Game(tetris_gui) 
    start = None
    
    while True:
        start = time.time()
        end = start
        while (end-start)<0.2:
            key = stdscr.getch()
            if key == 113: break
            if key == 114: break
            if not (key == -1):
                game.user_input(key)
            end = time.time()
            time.sleep(0.05)

        if key == 113:
            break
        if key == 114:
            game.reset()
            continue
        
        game.progress()
        
        if game.ended:
            break
        

if __name__ == "__main__":
    UI = "c"
    if UI == "c":
        os.system(f"printf '\033[8;{25};{50}t'")
        time.sleep(0.05)
        curses.wrapper(curses_main)
