import pyxel
from random import randint

TILE_SIZE = 4
TILE_NUM = 10
WINDOW_SIZE = TILE_SIZE*TILE_NUM

SNAKE_MIN_SIZE = 2

TEXT_OFFSET = -16

FLAME = 20

class SnakeHead:
    def __init__(self, x, y, direction, color):
        """

        :param x:
        :param y:
        :param direction: 蛇の向き 0:上 1:右 2:下 3:左
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.length = 3
        self.color = color
        self.body = None
        App.collision[self.x][self.y] = True

    def update(self, key_input):
        if (key_input - self.direction) % 4 != 2:
            self.direction = key_input

        self.body = SnakeBody(self.x, self.y, self.length, self.body, self.color)

        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        else:
            self.x -= 1

        # 回り込み
        self.x = self.x % TILE_NUM
        self.y = self.y % TILE_NUM

        # 当たり判定
        if App.collision[self.x][self.y]:
            App.game_over = True
        App.collision[self.x][self.y] = True

        # リンゴを食べる
        if App.apple and App.apple[0] == self.x and App.apple[1] == self.y:
            App.apple = None
            self.length += 1

        if self.body:
            self.body.update()

    def draw(self):
        pyxel.rect(self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE, self.color)
        if self.body:
            self.body.draw()


class SnakeBody:
    def __init__(self, x, y, length, next_body, color):
        self.x = x
        self.y = y
        self.length = length
        self.remain_time = length
        self.next_body = next_body
        self.color = color

    def update(self):
        self.remain_time -= 1

        if self.next_body:
            if self.next_body.remain_time < 0:
                self.next_body.delete()
                self.next_body = None
            else:
                self.next_body.update()

    def draw(self):
        size = self.remain_time / self.length * (TILE_SIZE - SNAKE_MIN_SIZE) + SNAKE_MIN_SIZE
        offset = (TILE_SIZE - size) // 2
        pyxel.rect(self.x*TILE_SIZE + offset, self.y*TILE_SIZE + offset, size, size, self.color)
        if self.next_body:
            self.next_body.draw()

    def delete(self):
        App.collision[self.x][self.y] = False


class App:
    collision = [[False]*TILE_NUM for _ in range(TILE_NUM)]
    game_over = False
    apple = [TILE_NUM//2, TILE_NUM//2]

    def __init__(self):
        pyxel.init(WINDOW_SIZE, WINDOW_SIZE)
        self.snake = SnakeHead(3, 0, 2, 5)
        self.step = 0
        self.key = 0
        pyxel.run(self.update, self.draw)


    def update(self):
        if App.game_over:
            pass
        else:
            if pyxel.btn(pyxel.KEY_UP):
                self.key = 0
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.key = 1
            if pyxel.btn(pyxel.KEY_DOWN):
                self.key = 2
            if pyxel.btn(pyxel.KEY_LEFT):
                self.key = 3

            if self.step < FLAME:
                self.step += 1
            else:
                self.snake.update(self.key)
                self.step = 0

            # リンゴの生成
            if not App.apple:
                App.apple = [0, 0]
                while True:
                    App.apple[0] = randint(0, TILE_NUM - 1)
                    App.apple[1] = randint(0, TILE_NUM - 1)
                    if not App.collision[App.apple[0]][App.apple[1]]:
                        break



    def draw(self):
        pyxel.cls(0)
        if App.game_over:
            pyxel.text(WINDOW_SIZE // 2 + TEXT_OFFSET  + randint(-1, 1), WINDOW_SIZE // 2 + randint(-1, 1), "GAMEOVER", 10)
            pyxel.text(WINDOW_SIZE // 2 + TEXT_OFFSET, WINDOW_SIZE // 2, "GAMEOVER", 7)
        else:
            self.snake.draw()
            if App.apple:
                pyxel.rect(App.apple[0] * TILE_SIZE, App.apple[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE, 8)


App()