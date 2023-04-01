import random
import curses
import time


class Shape:
    def __init__(self):
        self.direction = 0
        self.squares = []
        self.position_x = 4
        self.position_y = 0
        self.width = 1
        
    
    def move_down(self):
        self.position_y += 1
        
    def move_left(self):
        self.position_x -= 1
        
    def move_right(self):
        self.position_x += 1
        
    
class O_Block(Shape):
    def __init__(self):
        super(O_Block, self).__init__()
        self.squares = [[0,0],[0,1],[1,0],[1,1]]
        self.width = 2
        

    def rotate(self):
        return
    

class I_Block(Shape):
    def __init__(self):
        super(I_Block, self).__init__()
        self.squares = [[0,0],[1,0],[2,0],[3,0]]
        self.width = 1
    

    def rotate(self):
        # TODO: implement I rotation
        if self.direction == 0:
            self.squares = [[0,0],[0,1],[0,2],[0,3]]
            self.direction = 1
            return
        self.squares = [[0,0],[1,0],[2,0],[3,0]]
        self.direction = 0
    

class T_Block(Shape):
    def __init__(self):
        super(T_Block, self).__init__()
        self.squares = [[0,0],[0,1],[0,2],[1,1]]
        self.width = 1
    

    def rotate(self):
        if self.direction == 0:
            self.squares = [[0,0],[1,0],[1,1],[2,0]]
            self.direction = 1
        elif self.direction == 1:
            self.squares = [[1,0],[0,1],[1,1],[1,2]]
            self.direction = 2
        elif self.direction == 2:
            self.squares = [[0,1],[1,0],[1,1],[2,1]]
            self.direction = 3
        elif self.direction == 3:
            self.squares = [[0,0],[0,1],[0,2],[1,1]]
            self.direction = 0
        return
    

# TODO: add the remaining 4 blocks    
# TODO: check if the rotation is possible before rotating - it might need the change in structure of the code
# TODO: maybe flash a row that is full
# TODO: add docummentation to the classes


class Game():
    def __init__(self, stdscr):
        self.speed = 1
        self.score = 0
        self.height = 25
        self.width = 10
        self.stdscr = stdscr
        self.objects = []
        self.current_object = None
        self.left_offset = 4
        self.upper_offset = 2
        self.pad = curses.newpad(26, 21)
        self._draw_game()
        self.stdscr.refresh()
        # self.draw_win_test()
        self.current_object = self.generate_object()
        self.draw_object(self.current_object)
        self.free_squares = [[i,j] for j in range(self.width) for i in range(-5,21)]
    
    
    def can_move_down(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.squares:
            if not [-square[0]+y+1,square[1]+x] in self.free_squares:
                return False
        return True

    
    def can_move_right(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.squares:
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
        for square in obj.squares:
            if not [-square[0]+y,square[1]-1+x] in self.free_squares:
                return False
        return True

    def generate_object(self):
        gen = random.randint(0,2)
        if gen == 0:
            return O_Block()
        if gen == 1:
            return I_Block()
        if gen == 2:
            return T_Block()
        if gen == 3:
            return
        if gen == 4:
            return
        if gen == 5:
            return
        if gen == 6:
            return


    def place_object(self):
        self.objects.append(self.current_object)
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.squares:
            self.free_squares.remove([-square[0]+y,square[1]+x])
        self.current_object = self.generate_object()
            
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
            full_lines = self.get_full_lines()
            if full_lines:
                self.remove_and_move_lines(full_lines)
            return        
        self.current_object.move_down()
        self.draw_pad()
    

    def draw_taken_squares(self):
        for i in range(1,21):
            for j in range(10):
                # if [i,j] in self.free_squares: continue
                if [i,j] in self.free_squares: 
                    self.pad.addstr(i+4,j*2, " . ")
                    continue
                self.pad.addstr(i+4,j*2,"|@|")



    
    def draw_pad(self):
        self.pad.clear()
        # self.draw_objects()
        self.draw_taken_squares()
        self.draw_object(self.current_object) 
  

  
    def draw_win_test(self):
        for i in range(25):
            for j in range(20):
                self.pad.addstr(i,j,"@")
        self.pad.refresh(5, 1, self.upper_offset, self.left_offset+1 ,20+self.upper_offset ,19+self.left_offset)
        

    def _draw_game(self):
        self.stdscr.clear()
        for i in range(21):
            self.stdscr.addstr(i+self.upper_offset, self.left_offset,"|")
            self.stdscr.addstr(i+self.upper_offset, 20+self.left_offset,"|")
            
        for i in range(19):   
            self.stdscr.addstr(20+self.upper_offset, i+self.left_offset+1,"-")
            
            
    def draw_object(self,obj):
        for square in obj.squares:
            row = obj.position_y-square[0]+4
            col = obj.position_x+square[1]
            self.pad.addstr(row,col*2,"|#|")      

        self.pad.refresh(5, 1, self.upper_offset, self.left_offset+1 ,20+self.upper_offset-1 ,19+self.left_offset)
    

    def draw_objects(self):
        for obj in self.objects:
            self.draw_object(obj)
         
         
    def rotate(self):
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
    stdscr.resize(40,40)
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
