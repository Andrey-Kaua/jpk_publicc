import gun 
from engine import sprite, shapes, label, clock


class Player(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.INIT_HEALTH = 3
        self.INIT_SPEED = self.speed
        self.INIT_POS = (self.y, self.x)
        self.INIT_DIRECTION = self.direction

        self.alive = False
        self.health = self.INIT_HEALTH
        self.score = 0
        self.gun = gun.Gun(self.window, self)
        self.bullets = []
        
    def hard_reset(self):
        self.health = self.INIT_HEALTH
        self.score = 0
        self.soft_reset()

    def soft_reset(self):
        self.unrender()
        self.speed = self.INIT_SPEED
        self.y, self.x = self.INIT_POS
        self.direction = self.INIT_DIRECTION
        self.gun.reset()

    def check_bounds(self):
        if self.x < 1:
            self.x = 1
        if self.x + self.width - 1 > self.window.right_border:
            self.x = self.window.right_border - self.width
        if self.y < 1:
            self.y = 1
        if self.y + self.height - 1 > self.window.down_border:
            self.y = self.window.down_border - self.height

    def update(self, dt):
        self.unrender()
        self.y += self.direction[0] * self.speed[0] * dt
        self.x += self.direction[1] * self.speed[1] * dt
        self.check_bounds()
        self.gun.update(dt)

    def shoot(self, direction=[0,1]):
        self.gun.shoot(direction)
