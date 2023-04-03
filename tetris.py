import random
import curses
import time


class Shape:
    """
    A class that represents a tetris object. Classes of all of the main 7 tetris shapes are derived from this class.
    
    ...
        
    Attributes
    ----------
    direction : int
        This integer hold the information about how is the shape oriented. It can have values 0, 1, 2 or 3, but for
        some shapes the number of possible values is reduced thanks to symmetry. For example O_Block, which is a box
        of two by two squares looks the same no matter how it is rotated. The program is therefore simplified if we
        do not always consider all four possibilites.
    
    rotations : int
        Number of posible orientations an object can have.
    
    position_x : int
        X coordinate of the bottom left corner of the object.
    
    position_y : int
        Y coordinate of the bottome left corner of the object.
    
    squares : list of lists of lists of int
        The first index chooses a direction. That is the first extraction by which we get a list of squares which make
        an object in the chosen orietation. Each square is a list of two integers [y_coordiate, x_coordinate] relative 
        to the base point which is the bottom left corner of the object. These lists do not change during the game.
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
        self.position_x = 5  # Initialize position x so that it starts in the middle
        self.position_y = 0  # Initialize position y so that it start outside of the visible field
        
    def move_down(self):
        """Function that represnts 'down' movement of the object.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_y += 1
        
    def move_left(self):
        """Function that represnts 'left' movement of the object.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_x -= 1
        
    def move_right(self):
        """Function that represnts 'right' movement of the object.
        
        Parameters
        ----------
        no parameters
        
        Returns
        -------
        nothing"""
        self.position_x += 1

    def get_squares(self,rotated=False):
        """'The getter' of list of the squares that represent the shape of the object.
        
        Parameters
        ----------
        rotated : bool, optional 
            When True, the returned list of squares is not of the current orientation but of a clock-wisely rotated one.
            
        Returns
        -------
        list of squares that represent the shape of the object. If rotated is not stated or is False, the returned shape
        corresponds to the current orientation of the object represented by the attribute 'self.direction'.
        """
        if not rotated:
            return self.squares[self.direction]
        return self.squares[self.direction-self.rotations+1]
    
    
class O_Block(Shape):
    def __init__(self):
        super(O_Block, self).__init__()
        self.squares.append([[0,0],[0,1],[1,0],[1,1]])
        
    def rotate(self):
        return


class I_Block(Shape):
    def __init__(self):
        super(I_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[0,0],[1,0],[2,0],[3,0]])  
        self.squares.append([[0,0],[0,1],[0,2],[0,3]])

    def rotate(self):
        if not self.direction:
            self.direction = 1
            return
        self.direction = 0
    

class T_Block(Shape):
    def __init__(self):
        super(T_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,0], [0,1], [0,2], [1,1]])
        self.squares.append([[0,0], [1,0], [1,1], [2,0]])
        self.squares.append([[1,0], [0,1], [1,1], [1,2]])
        self.squares.append([[0,1], [1,0], [1,1], [2,1]])

    def rotate(self):
        self.direction = (self.direction+1)%4
        return
    
class Z_Block(Shape):
    def __init__(self):
        super(Z_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[1,0], [0,1], [1,1], [0,2]])
        self.squares.append([[0,0], [1,0], [1,1], [2,1]])
    
    def rotate(self):
        if not self.direction:
            self.direction = 1
            return
        self.direction = 0
    
class S_Block(Shape):
    def __init__(self):
        super(S_Block, self).__init__()
        self.rotations = 2
        self.squares.append([[0,0], [0,1], [1,1], [1,2]])
        self.squares.append([[0,1], [1,0], [1,1], [2,0]])
    
    def rotate(self):
        if not self.direction:
            self.direction = 1
            return
        self.direction = 0
    
class L_Block(Shape):
    def __init__(self):
        super(L_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,0], [0,1], [1,0], [2,0]])
        self.squares.append([[0,0], [1,0], [1,1], [1,2]])
        self.squares.append([[0,1], [1,1], [2,1], [2,0]])
        self.squares.append([[0,0], [0,1], [0,2], [1,2]])
    
    def rotate(self):
        self.direction = (self.direction+1)%4
        return
    
    
    
class J_Block(Shape):
    def __init__(self):
        super(J_Block, self).__init__()
        self.rotations = 4
        self.squares.append([[0,1], [1,1], [2,1], [0,0]])
        self.squares.append([[0,0], [0,1], [0,2], [1,0]])
        self.squares.append([[0,0], [2,1], [1,0], [2,0]])
        self.squares.append([[0,2], [1,0], [1,1], [1,2]])
    
    def rotate(self):
        self.direction = (self.direction+1)%4
        return

# TODO: if the rotation is not possible, check whether it is not possible after moving it left once or twice 
# TODO: maybe flash a row that is full
# TODO: add docummentation to the classes
# TODO: configure a pad with next block so that it looks nice
# TODO: configure a pad with the score so that it looks nice


class Game():
    def __init__(self, stdscr):
        self.speed = 1
        self.score = 0
        self.height = 25
        self.width = 10
        self.stdscr = stdscr
        self.objects = []
        self.current_object = None
        self.next_object = self.generate_object()
        self.left_offset = 4
        self.upper_offset = 2
        self.main_pad = curses.newpad(26, 21)
        self.score_pad = curses.newpad(5, 5)
        self.next_pad = curses.newpad(8,16)
        self._draw_game()
        # self.stdscr.refresh()
        # self.draw_win_test()
        self.current_object = self.generate_object()
        self.draw_object(self.current_object)
        self.free_squares = [[i,j] for j in range(self.width) for i in range(-5,21)]
    
    
    def update_next_object(self):
        obj = self.next_object = self.generate_object()
        self.next_pad.clear()
        for square in obj.get_squares():
            row = -square[0]+4
            col = 2+square[1]
            self.next_pad.addstr(row,col*2,"|#|")      

        self.next_pad.refresh(0, 0, 8, 30 ,15 ,45)
        

    
    def update_score(self, erased_lines):
        if erased_lines == 1:
            self.score += 1
        elif erased_lines == 2:
            self.score += 4
        elif erased_lines == 3:
            self.score += 16
        elif erased_lines == 4:
            self.score += 64
        
        
        self.score_pad.addstr(3,1,str(self.score))
        self.score_pad.refresh(0,0,20,30,24,34)
        
    def can_rotate(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.get_squares(rotated=True):
            if not [-square[0]+y, square[1]+x] in self.free_squares:
                return False
        return True
    
    def can_move_down(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.get_squares():
            if not [-square[0]+y+1,square[1]+x] in self.free_squares:
                return False
        return True

    
    def can_move_right(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.get_squares():
            if not [-square[0]+y,square[1]+x+1] in self.free_squares:
                return False
        return True
    
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
    
    def can_move_left(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.get_squares():
            if not [-square[0]+y,square[1]-1+x] in self.free_squares:
                return False
        return True

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
        self.objects.append(self.current_object)
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

            
    def progress(self):
        if not self.can_move_down():
            self.place_object()
            self.update_next_object()
            full_lines = self.get_full_lines()
            if full_lines:
                self.remove_and_move_lines(full_lines)
                self.update_score(len(full_lines))
            return        
        self.current_object.move_down()
        self.draw_pad()
    

    def draw_taken_squares(self):
        for i in range(1,21):
            for j in range(10):
                # if [i,j] in self.free_squares: continue
                if [i,j] in self.free_squares: 
                    self.main_pad.addstr(i+4,j*2, " . ")
                    continue
                self.main_pad.addstr(i+4,j*2,"|@|")


    
    def draw_pad(self):
        self.main_pad.clear()
        # self.draw_objects()
        self.draw_taken_squares()
        self.draw_object(self.current_object) 
  

  
    def draw_win_test(self):
        for i in range(25):
            for j in range(20):
                self.main_pad.addstr(i,j,"@")
        self.main_pad.refresh(5, 1, self.upper_offset, self.left_offset+1 ,20+self.upper_offset ,19+self.left_offset)
        

    def _draw_game(self):
        self.stdscr.clear()
        for i in range(21):
            self.stdscr.addstr(i+self.upper_offset, self.left_offset,"|")
            self.stdscr.addstr(i+self.upper_offset, 20+self.left_offset,"|")
            
        for i in range(19):   
            self.stdscr.addstr(20+self.upper_offset, i+self.left_offset+1,"-")
        self.stdscr.refresh()
        
        self.score_pad.addstr(3,1,str(self.score))
        self.score_pad.refresh(0,0,20,30,24,34)
        
        self.update_next_object()
        
    def draw_object(self,obj):
        for square in obj.get_squares():
            row = obj.position_y-square[0]+4
            col = obj.position_x+square[1]
            self.main_pad.addstr(row,col*2,"|#|")      

        self.main_pad.refresh(5, 1, self.upper_offset, self.left_offset+1 ,20+self.upper_offset-1 ,19+self.left_offset)
    

    def draw_objects(self):
        for obj in self.objects:
            self.draw_object(obj)
         
         
    def rotate(self):
        if not self.can_rotate(): return
        self.current_object.rotate()     


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
            
        self.draw_pad()
           
    
def main(stdscr):
    stdscr.clear()
    stdscr.resize(40,50)
    stdscr.nodelay(1)
    game = Game(stdscr) 
    start = None
    
    while True:
        start = time.time()
        end = start
        while (end-start)<0.2:
            key = stdscr.getch()
            if key == 113: break
            if not (key == -1):
                game.user_input(key)
            end = time.time()
            time.sleep(0.05)

        if key == 113:
            break
        
        game.progress()
        

curses.wrapper(main)
