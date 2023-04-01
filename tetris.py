import random
import curses
import time


class Shape:
    def __init__(self):
        self.direction = 0
        self.squares = []
        self.position_x = 0
        self.position_y = 0
        self.width = 1
        
    def rotateRight(self):
        self.direction = (self.direction+1)//4
        
    def rotateLeft(self):
        self.direction = (self.direction+3)//4
        
    def move_down(self):
        self.position_y += 1
        
    def move_left(self):
        if self.position_x < 1: return
        self.position_x -= 1
        
    def move_right(self):
        if self.position_x+self.width > 9: return
        self.position_x += 1
        
    
class O_Block(Shape):
    def __init__(self):
        super(O_Block, self).__init__()
        self.squares = [[0,0],[0,1],[1,0],[1,1]]
        self.width = 2
        
    def rotate():
        return
    
class I_Block(Shape):
    def __init__(self):
        super(I_Block, self).__init__()
        self.squares = [[0,0],[1,0],[2,0],[3,0]]
        self.width = 1
    
    def rotate():
        # TODO: implement I rotation
        return
    
class Game():
    def __init__(self, stdscr):
        self.speed = 1
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
        self.free_squares = [[i,j] for j in range(10) for i in range(-5,21)]
    
    
    def can_move_down(self):
        obj = self.current_object
        x = obj.position_x
        y = obj.position_y
        for square in obj.squares:
            if not [-square[0]+y+1,square[1]+x] in self.free_squares:
                return False
        return True

    def generate_object(self):
        gen = random.randint(0,1)
        if gen == 0:
            return O_Block()
        if gen == 1:
            return I_Block()

        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.squares:
            if not [-square[0]+y+1,square[1]+x] in self.free_squares:
                return False
        return True


    def place_object(self):
        self.objects.append(self.current_object)
        x = self.current_object.position_x
        y = self.current_object.position_y
        for square in self.current_object.squares:
            self.free_squares.remove([-square[0]+y,square[1]+x])
        self.current_object = self.generate_object()
            
    
    def progress(self):
        if not self.can_move_down():
            self.place_object()
            return        
        self.current_object.move_down()
        self.draw_pad()
    

    def draw_pad(self):
        self.pad.clear()
        self.draw_objects()
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
            
    def user_input(self, key):
        if key == curses.KEY_RIGHT:
            self.current_object.move_right()
        elif key == curses.KEY_LEFT:
            self.current_object.move_left()
            
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
        while (end-start)<0.1:
            key = stdscr.getch()
            if key == 113: break
            if not (key == -1):
                game.user_input(key)
            end = time.time()
            time.sleep(0.01)

        if key == 113:
            break
        
        game.progress()
        

curses.wrapper(main)

