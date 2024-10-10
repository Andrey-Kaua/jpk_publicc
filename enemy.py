from engine import sprite, label
from random import randint
from math import ceil

class Enemy(sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.INIT_HEALTH = 4
		self.INIT_SPEED = self.speed
		self.INIT_COLOR = self.color_pair

		self.health = self.INIT_HEALTH
		self.points = 40
		
	def reset(self):
		self.health = self.INIT_HEALTH
		self.color_pair = self.INIT_COLOR
		self.unrender()
		self.y, self.x = self.rng_pos()

	def check_bounds(self):
		player = self.window.player
		if self.is_collided_with(player):
			player.health -= 1
			if player.health <= 0: 
				player.alive = False
			player.soft_reset()
			for ene in self.group:
				ene.reset()

		collided_bullet = self.check_group_collision(self.window.player.bullets)
		if collided_bullet:
			self.health -= 1
			if self.health <= 0:
				sprite.Sprite(window=self.window, x=self.x-1, y=self.y-1, images=self.window.explosion_imgs, color_pair=((255, 0, 0), None), group=self.window.explosions)
				self.window.player.score += self.points
				self.reset()
			if self.health <= ceil((1/4)*self.health):
				self.color_pair = ((255, 0, 0), None)
			elif self.health <= ceil((3/4)*self.health):
				self.color_pair = ((255, 255, 0), None)
			collided_bullet.unrender()
			self.window.player.bullets.remove(collided_bullet)
	
	def movement(self):
		if self.y + self.images[0].height >= self.window.down_border:
			self.direction = [-1, 0]
		elif self.y <= 1:
			self.direction = [1, 0]
		elif self.x + self.images[0].width >= self.window.right_border:
			self.direction = [0, -1]
		elif self.x <= 1:
			self.direction = [0, 1]
		else:
			player = self.window.player
			y = player.y - self.y
			x = player.x - self.x
			tg = 1 if x == 0 else y/x
			self.direction = [0, x/abs(x)] if abs(tg) < 0.5 else [y/abs(y), 0]
		
	def update(self, dt):
		self.unrender()
		self.movement()
		self.y += self.direction[0] * self.speed[0] * dt
		self.x += self.direction[1] * self.speed[1] * dt
		self.check_bounds()
	
	def rng_pos(self):
		rng_side = randint(1,4)
		d_border, r_border = self.window.down_border, self.window.right_border
		match rng_side:
			case 1:
				rng_y = randint(- self.images[0].height - 10, - self.images[0].height)
				rng_x = randint(1, r_border - 1 - self.images[0].width)
			case 2:
				rng_y = randint(1, d_border - 1 - self.images[0].height)
				rng_x = randint(r_border, r_border + 10)
			case 3:
				rng_y = randint(d_border, d_border + 10)
				rng_x = randint(1, r_border - 1 - self.images[0].width)
			case 4:
				rng_y = randint(1, d_border - 1 - self.images[0].height)
				rng_x = randint(- self.images[0].width - 10, - self.images[0].width)
		choords = [rng_y, rng_x]
		return choords
	
	def unrender(self):
		self.render_or_not(render=False)
		