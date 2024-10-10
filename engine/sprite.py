from . import shapes, sprite, clock
from math import floor

class Sprite:
    def __init__(self, window, y=0, x=0, direction=[0, 0], speed=[0, 0], images=[], image_num=0, color_pair=None, group=None):
        self.window = window
        self.y, self.x = y, x
        self.direction = list(direction)
        self.speed = list(speed)

        if color_pair != None:
            self.color_pair = tuple(color_pair)
        else:
            self.color_pair = color_pair

        self.images = images
        self.image_num = image_num

        self.source = self.images[self.image_num].source
        self.width = self.images[self.image_num].width
        self.height = self.images[self.image_num].height
        self.image = self.images[self.image_num].value

        self.animation_clock = clock.Clock()

        self.group = group
        if type(self.group) == list:
            self.group.append(self)

    def render_or_not(self, render):
        for y in range(len(self.image)):
            for x in range(len(self.image[y])):
                pixel_y = floor(self.y) + y
                pixel_x = floor(self.x) + x
                char = self.image[y][x] if render else self.window.char
                color = self.color_pair if render else self.window.color_pair
                if self.image[y][x] != " " and 0 <= pixel_x <= self.window.width and 0 <= pixel_y <= self.window.height:
                    is_changed = not(self.window.screen_array[pixel_y][pixel_x][1:] == [char, color])
                    if not is_changed:
                        is_changed = self.window.screen_array[pixel_y][pixel_x][0]
                    self.window.screen_array[pixel_y][pixel_x] = [is_changed, char, color]

    def render(self):
        self.render_or_not(render=True)

    def unrender(self):
        self.render_or_not(render=False)
    
    def update(self, dt):
        self.unrender()
        self.y += self.direction[0] * self.speed[0] * dt
        self.x += self.direction[1] * self.speed[1] * dt
        self.check_bounds()
    
    def check_bounds(self): 
        pass

    def is_collided_with(self, other):
        # if colliding horizontally AND colliding vertically AND other is a rectangle(bullet)/sprite(player)
        if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) and (isinstance(other, shapes.Rect) or isinstance(other, sprite.Sprite)):
            return other
        
    def check_group_collision(self, others):
        for obj in others:
            collided = self.is_collided_with(obj)
            if not(collided is self) and collided:
                return collided

    def destroy(self):  
        self.unrender()
        if self.group:
            self.group.remove(self)

    def animate(self, loop=True, fps=60):
        if self.animation_clock.get_dt() >= 1 / fps:
            if self.image_num == len(self.images):
                if loop:
                    self.image_num = 0
                else:
                    self.destroy()
                    return
            self.unrender()
            self.source = self.images[self.image_num].source
            self.width = self.images[self.image_num].width
            self.height = self.images[self.image_num].height
            self.image = self.images[self.image_num].value
            self.image_num += 1
            self.animation_clock.update()
        self.render()
