import player, enemy, os, button
from engine import window, util, label, sprite
from curses.textpad import rectangle
from glob import glob
from random import randint

class GameWindow(window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.RANKING = "ranking/"
        self.USER = os.environ.get("USERNAME")
        self.LOCAL_RANKING_SOURCE = self.RANKING + self.USER + ".txt"

        self.explosion_imgs = util.load_images("assets/explosion")
        self.explosions = []

        TITLE_IMGS = util.load_images("./assets/title")

        self.title = sprite.Sprite(window=self, y=2, x=2, images=TITLE_IMGS)

        #region BUTTONS

        buttons_text = ["PLAY", "QUIT"]
        self.buttons = []
        for idx, txt in enumerate(buttons_text):
            button.Button(window=self, text=[txt], x=self.width // 2, y=self.height//2 + idx, anchor="center", color_pair=((0, 255, 0), None), group=self.buttons)
        self.buttons[0].active = True

        self.cursor = 0

        #endregion

        #region PLAYER

        PLAYER_INIT_CHOORDS = [self.down_border//2, self.right_border//2]
        PLAYER_INIT_DIRECTION = [0, 0]
        PLAYER_INIT_SPEED = [15, 30]
        PLAYER_IMGS = util.load_images("./assets/player")

        self.player = player.Player(window=self, y=PLAYER_INIT_CHOORDS[0], x=PLAYER_INIT_CHOORDS[1],
                                    direction=PLAYER_INIT_DIRECTION, speed=PLAYER_INIT_SPEED, images=PLAYER_IMGS)
        
        #endregion

        #region ENEMIES
        
        ENEMY_IMGS = util.load_images("./assets/enemy")
        ENEMY_INIT_DIRECTION = [1, 0]
        ENEMY_INIT_SPEED = [3, 6]
        self.enemies = []

        for i in range(10):
            rng_side = randint(1,4)
            match rng_side:
                case 1:
                    rng_y = randint(- ENEMY_IMGS[0].height - 10, - ENEMY_IMGS[0].height)
                    rng_x = randint(1, self.right_border - 1 - ENEMY_IMGS[0].width)
                case 2:
                    rng_y = randint(1, self.down_border - 1 - ENEMY_IMGS[0].height)
                    rng_x = randint(self.right_border, self.right_border + 10)
                case 3:
                    rng_y = randint(self.down_border, self.down_border + 10)
                    rng_x = randint(1, self.right_border - 1 - ENEMY_IMGS[0].width)
                case 4:
                    rng_y = randint(1, self.down_border - 1 - ENEMY_IMGS[0].height)
                    rng_x = randint(- ENEMY_IMGS[0].width - 10, -ENEMY_IMGS[0].width)
            ENEMY_INIT_CHOORDS = [rng_y, rng_x]
            enemy.Enemy(window=self, y=ENEMY_INIT_CHOORDS[0], x=ENEMY_INIT_CHOORDS[1], direction=ENEMY_INIT_DIRECTION, 
                        speed=ENEMY_INIT_SPEED, images=ENEMY_IMGS, group=self.enemies)

        #endregion

        #region LABELS

        self.labels = []

        self.text = label.Label(window=self, text=[f"bullets: {self.player.gun.bullet_count}"], y=self.height-15, x=1, group=self.labels)

        self.life = label.Label(window=self, text=[f"life: {self.player.health}"], y=self.height-14, x=1, group=self.labels)

        self.score = label.Label(window=self, text=[f"score: "], y=self.height-13, x=1, group=self.labels)

        self.ranking = label.Label(window=self, text=[f"RANKING"], y=self.height//2 - 7, x=self.width//5, anchor="center", group=self.labels)

        #endregion

    def handle_key_events(self, key):
        self.player.direction = [0, 0]
        shoot_direction = [None, None]
        if self.player.alive:
            match key:
                case "q":
                    return -1
                case "w":
                    self.player.direction = [-1, 0]
                case "s":
                    self.player.direction = [1, 0]
                case "d":
                    self.player.direction = [0, 1]
                case "a":
                    self.player.direction = [0, -1]
                
                case "key_up":
                    shoot_direction = [-1, 0]
                    self.player.shoot(shoot_direction)
                case "key_down":
                    shoot_direction = [1, 0]
                    self.player.shoot(shoot_direction)
                case "key_right":
                    shoot_direction = [0, 1]
                    self.player.shoot(shoot_direction)
                case "key_left":
                    shoot_direction = [0, -1]
                    self.player.shoot(shoot_direction)
        else:
            match key:
                case "q":
                    return -1
                case "key_up":
                    self.buttons[self.cursor].active = False
                    self.buttons[self.cursor].update()
                    self.cursor -= 1
                case "key_down":
                    self.buttons[self.cursor].active = False
                    self.buttons[self.cursor].update()
                    self.cursor += 1
                case "e":
                    if self.cursor == 0:
                        self.reset()
                        self.buttons[1].active = False
                        self.player.alive = True
                        self.cursor = 0
                        self.player.hard_reset()
                    elif self.cursor == 1:
                        return -1

            if self.cursor < 0:
                self.cursor = len(self.buttons) - 1
            if self.cursor > len(self.buttons) - 1:
                self.cursor = 0
            self.buttons[self.cursor].active = True
            self.buttons[self.cursor].update()

    def get_local_ranking(self):
        ranking = [] #list of integers
        
        if not os.path.isfile(self.LOCAL_RANKING_SOURCE):
            open(self.LOCAL_RANKING_SOURCE, "x")
        
        with open(self.LOCAL_RANKING_SOURCE, "r") as file:
            for line in file.read().split("\n")[:-1]:
                ranking.append(int(line))
        
        return ranking

    def update_local_ranking(self):
        score = self.player.score

        ranking = self.get_local_ranking()

        if score not in ranking:
            ranking.append(score)
        ranking.sort(reverse=True)
        
        with open(self.LOCAL_RANKING_SOURCE, "w") as file:
            for score in ranking:
                file.write(f"{score}\n")
        
        ranking_text = []
        for i in range(min(10, len(ranking))):
            ranking_text.append(f'{i+1}. {ranking[i]:0>6}')

    def get_global_ranking(self):
        global_ranking = []

        ranking_list = glob(self.RANKING+"*")
        for local_ranking in ranking_list:
            with open(local_ranking) as file:
                file_lines = file.read().split("\n")[:-1]
                for i in range(min(10, len(file_lines))):
                    score = file_lines[i]
                    global_ranking.append([int(score), local_ranking[len(self.RANKING):-4]])
        
        global_ranking.sort(reverse=True)
        global_ranking = global_ranking[:10]

        text = []
        for i in range(len(global_ranking)):
            text.append("")
            text.append(f"{i+1:>2}.  {global_ranking[i][1]:<24} {global_ranking[i][0]:0>8}")

        return text

    def run(self):
        global_ranking = self.get_global_ranking()

        while self.running:
            dt = self.clock.get_dt()
            try:
                key = self.screen.getkey().lower()
            except:
                key = None
            result = self.handle_key_events(key)
            if result == -1:
                break
        
            if not self.player.alive:
                self.ranking.update(["RANKING"]+global_ranking)
                self.ranking.render()
                self.title.render()
                for btn in self.buttons:
                    btn.update()
                    btn.render()
            else:
                self.title.unrender()
                self.player.update(dt)
                self.player.animate(loop=True, fps=8)

                for bullet in self.player.bullets:
                    bullet.update(dt)
                    if bullet.exists:
                        bullet.render()

                self.score.update([f"score: {self.player.score}"])
                self.life.update([f"life: {self.player.health}"])
                self.score.render()
                self.life.render()

                for ene in self.enemies:
                    ene.update(dt)
                    if not self.player.alive:
                        self.update_local_ranking()
                        global_ranking = self.get_global_ranking()
                        for label in self.labels:
                            label.unrender()
                        self.reset()
                        break
                    ene.render()
                
                for exp in self.explosions:
                    exp.animate(loop=False, fps=self.fps/3)

                rectangle(self.screen, 0, 0, self.down_border, self.right_border)
            self.update(self.fps)


game = GameWindow()
game.start(game.run)
