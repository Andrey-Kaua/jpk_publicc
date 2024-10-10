from math import floor

class Label:
    def __init__(self, window, text=[""], y=0, x=0, anchor="left", color_pair=None, group=None):
        self.window = window
        self.text = text
        self.y, self.x = y, x
        self.d_border, self.r_border = self.window.down_border, self.window.right_border
        self.anchor = anchor
        if color_pair != None:
            self.color_pair = tuple(color_pair)
        else:
            self.color_pair = color_pair
        self.group = group
        if type(self.group) == list:
            self.group.append(self)

    def update(self, new_text=None):
        self.unrender()
        if new_text:
            self.text = new_text[:]

    def change_pixel(self, y, x, char, color_pair):
        if 0 <= x <= self.r_border and 0 <= y <= self.d_border:
            is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
            if not is_changed:
                is_changed = self.window.screen_array[y][x][0]
            self.window.screen_array[y][x] = [is_changed, char, color_pair]

    def render_text(self, color_pair, render):
        if self.anchor == "left": x_start = floor(self.x)
        for y in range(len(self.text)):
                line = self.text[y]
                pixel_y = floor(self.y) + y
                if self.anchor == "center": x_start = floor(self.x) - (len(line) - 1) // 2
                for x in range(len(line)):
                    pixel_x = x_start + x
                    char_to_render = line[x] if render else self.window.char
                    self.change_pixel(y=pixel_y, x=pixel_x, char=char_to_render, color_pair=color_pair)

    def unrender(self):
        self.render_text(color_pair=self.window.color_pair, render=False)

    def render(self):
        self.render_text(color_pair=self.color_pair, render=True)

    def destroy(self):
        self.unrender()
        if self.group:
            self.group.remove(self)
    
    def update(self, new_text=None):
        self.unrender()
        if new_text:
            self.text = new_text[:]
