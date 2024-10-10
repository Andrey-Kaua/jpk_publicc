from engine import clock, shapes

class Bullet(shapes.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exists = True

    def check_bounds(self):
        if self.y < 1 or self.y > self.window.down_border or self.x < 1 or self.x > self.window.right_border:
            self.exists = False
            self.window.player.bullets.remove(self)


class Gun:
    def __init__(self, window, player):
        self.window = window
        self.player = player

        self.bullet_timer = clock.Timer()
        self.bullet_color_pair = ((255, 165, 0), None)

        self.INIT_COOLDOWN = 0.2
        self.INIT_BULLET_COUNT = 500
        self.INIT_BULLET_SPEED = (30, 60)
        self.INIT_BULLET_CHAR = "*"
        self.INIT_BULLET_WIDTH = 1
        self.INIT_BULLET_HEIGHT = 1

        self.cooldown = self.INIT_COOLDOWN        
        self.bullet_count = self.INIT_BULLET_COUNT
        self.bullet_speed = self.INIT_BULLET_SPEED
        self.bullet_char = self.INIT_BULLET_CHAR
        self.bullet_width = self.INIT_BULLET_WIDTH
        self.bullet_height = self.INIT_BULLET_HEIGHT
    
    def shoot(self, direction):
        if self.bullet_count > 0 and self.bullet_timer.count <= 0:
            self.bullet_timer.set_timer(self.cooldown)
            self.bullet_count -= 1
            bullet_shoot_pos = [self.player.y+1, self.player.x+self.player.width//2]

            Bullet(window=self.window, y=bullet_shoot_pos[0], x=bullet_shoot_pos[1], width=self.bullet_width, height=self.bullet_height, direction=direction,
                     speed=self.bullet_speed, char=self.bullet_char, group=self.player.bullets, color_pair=self.bullet_color_pair)
    
    def update(self, dt):
        self.bullet_timer.update(dt)

    def reset(self):
        self.cooldown = self.INIT_COOLDOWN
        self.bullet_count = self.INIT_BULLET_COUNT
        self.bullet_speed = self.INIT_BULLET_SPEED
        self.bullet_char = self.INIT_BULLET_CHAR
        self.bullet_width = self.INIT_BULLET_WIDTH
        self.bullet_height = self.INIT_BULLET_HEIGHT
        for bullet in self.player.bullets:
            bullet.unrender()
        self.player.bullets = []
