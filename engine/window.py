import curses as cs
from . import clock, util
from math import floor

class Window:
    def __init__(self, char=" ", fps = 40):
        self.screen = cs.initscr()
        self.height, self.width = cs.LINES - 2, cs.COLS - 1
        self.down_border, self.right_border = self.height, self.width
        self.char = char
        self.fps = fps

    def exit(self):
        self.running = "exit"
        cs.nocbreak()
        cs.echo()
        cs.endwin()

    def start(self, func):  
        try:
            cs.start_color()
            cs.noecho()
            cs.cbreak()
            cs.curs_set(0)
            self.clock = clock.Clock()
            self.can_change = cs.can_change_color()
            self.color_pair = ((255, 255, 255), (0, 0, 0))
            self.color_pairs = util.ColorPairs(self)
            self.color_pairs.add(self.color_pair)
            self.screen.keypad(True)
            self.screen.nodelay(True)
            self.running = True
            self.reset()
            func() # the main game loop
            self.exit()

        except Exception as e:
            self.exit()
            raise e
        
    def reset(self):
        self.screen_array = [] # 2D array of arrays, each with three values, flag, char, and color_pair
        # flag is a boolean that indicates whether that particular screen_arr value is changed/updated, thus needing rendering
        for i in range(floor(self.height)+1):
            self.screen_array.append([[True, self.char, self.color_pair] for j in range(floor(self.width)+1)])

    def update(self, fps):
        for y in range(floor(self.height)+1):
            for x in range(floor(self.width)+1):
                try:
                    if self.screen_array[y][x][0]: # if that particular point is changed...
                        if self.can_change:
                            color_pair = self.screen_array[y][x][2]
                            if color_pair:
                                self.screen.addstr(y, x, self.screen_array[y][x][1], self.color_pairs.get_color_pair(color_pair))
                            else:
                                self.screen_array[y][x][2] = self.color_pair
                                self.screen.addstr(y, x, self.screen_array[y][x][1], self.color_pairs.get_color_pair(self.color_pair))
                        else:
                            self.screen.addstr(y, x, self.screen_array[y][x][1], cs.color_pair(0))
                    self.screen_array[y][x][0] = False
                except:
                    # this happens when the terminal size is smaller than the self.screen_array size
                    # self.screen.resize(floor(self.height), floor(self.width))
                    self.exit()
        self.screen.refresh()
        self.clock.update()
        self.clock.delay(1 / fps)
