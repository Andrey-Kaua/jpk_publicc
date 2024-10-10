from . import sprite, clock, shapes
from math import floor

class Rect:
    def __init__(self, window, y=0, x=0, width=1, height=1, direction=[0, 0], speed=[0, 0], char="*", fill=True, color_pair=None, group=None):
        self.window = window
        self.y, self.x = y, x
        self.width, self.height = width, height
        self.d_border, self.r_border = self.window.down_border, self.window.right_border
        self.direction = list(direction)
        self.speed = list(speed)
        
        self.char = char
        self.fill = fill
        
        if color_pair != None:
            self.color_pair = tuple(color_pair)
        else:
            self.color_pair = color_pair
        
        self.group = group
        if type(self.group) == list:
            self.group.append(self)

    def choords_processing(self):
        y1 = floor(self.y) if floor(self.y) > 0 else 0
        y2 = floor(self.y + self.height) - 1 if floor(self.y + self.height) - 1 < self.d_border else self.d_border
        x1 = floor(self.x)
        x2 = floor(self.x + self.width - 1)
        return y1, y2, x1, x2

    def change_pixel(self, y, x, char, color_pair):
        if 0 <= x <= self.r_border and 0 <= y <= self.d_border:
            is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
            if not is_changed:
                is_changed = self.window.screen_array[y][x][0]
            self.window.screen_array[y][x] = [is_changed, char, color_pair]

    def draw_line(self, x1, x2, y, char, color_pair):
        for x in range(x1, x2 + 1):
            self.change_pixel(y=y, x=x, char=char, color_pair=color_pair)

    def draw_endpoints(self, x1, x2, y, char, color_pair):
        self.change_pixel(y=y, x=x1, char=char, color_pair=color_pair)
        self.change_pixel(y=y, x=x2, char=char, color_pair=color_pair)

    def render_char(self, char, color_pair):
        y1, y2, x1, x2 = self.choords_processing()
        for y in range(y1, y2 + 1):
            if self.fill:
                self.draw_line(x1, x2, y, char, color_pair)
            else:
                if y == y1 or y == y2:
                    self.draw_line(x1, x2, y, char, color_pair)
                else:
                    self.draw_endpoints(x1, x2, y, char, color_pair)

    def render(self):
        self.render_char(char=self.char, color_pair=self.color_pair)

    def unrender(self):
        self.render_char(char=self.window.char, color_pair=self.window.color_pair)

    def check_bounds(self):
        pass

    def update(self, dt):
        self.unrender()
        self.y += self.direction[0] * self.speed[0] * dt
        self.x += self.direction[1] * self.speed[1] * dt
        self.check_bounds()

    def is_collided_with(self, other):
        # if colliding horizontally AND colliding vertically AND other is a rectangle(bullet)/sprite(player)
        if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) and (isinstance(other, shapes.Rect) or isinstance(other, sprite.Sprite)):
            return other
        
    def check_group_collision(self, others):
        for obj in others:
            collided = self.is_collided_with(obj)
            if not(collided is self) and collided:
                return collided
