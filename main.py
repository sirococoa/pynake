import pyxel
from random import randint

TILE_SIZE = 8
TILE_NUM = 10
WINDOW_SIZE = TILE_SIZE*TILE_NUM

SNAKE_MIN_SIZE = 2

MAX_FLAME = 20
MIN_FLAME = 5

MAX_SPEED_LENGTH = 25

def text_mc(x, y, text_list, color_list):
    TEXT_W = 4
    for i, s in enumerate(text_list):
        pyxel.text(x, y, s, color_list[i])
        x += len(s) * TEXT_W

def center(text, width):
    TEXT_W = 4
    return width // 2 - len(text) * TEXT_W // 2

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
        connection = (self.direction + 2) % 4

        if (key_input - self.direction) % 4 != 2:
            self.direction = key_input

        self.body = SnakeBody(self.x, self.y, self.length, self.body, self.color, (self.direction, connection))

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
    def __init__(self, x, y, length, next_body, color, connection):
        self.x = x
        self.y = y
        self.length = length
        self.remain_time = length
        self.next_body = next_body
        self.color = color
        self.connection = connection

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
        size = size // 2 * 2 # 2の倍数に調整
        offset = (TILE_SIZE - size) // 2
        pyxel.rect(self.x * TILE_SIZE + offset, self.y * TILE_SIZE + offset, size, size, self.color)
        if 0 in self.connection:
            pyxel.rect(self.x * TILE_SIZE + offset, self.y * TILE_SIZE, size, offset, self.color)
        if 1 in self.connection:
            pyxel.rect(self.x * TILE_SIZE + offset + size, self.y * TILE_SIZE + offset, offset, size, self.color)
        if 2 in self.connection:
            pyxel.rect(self.x * TILE_SIZE + offset, self.y * TILE_SIZE + offset + size, size, offset, self.color)
        if 3 in self.connection:
            pyxel.rect(self.x * TILE_SIZE, self.y * TILE_SIZE + offset, offset, size, self.color)
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
        self.snake1 = SnakeHead(3, 0, 2, 5)
        self.snake2 = SnakeHead(TILE_NUM - 4, TILE_NUM - 1, 0, 10)
        self.step = 0
        self.key = 0
        self.flame = 20
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

            if self.step < self.flame:
                self.step += 1
            else:
                self.snake1.update(self.key)
                self.snake2.update((self.key + 2) % 4)
                self.step = 0
                self.flame = (MAX_FLAME - MIN_FLAME) * (MAX_SPEED_LENGTH - min(self.snake1.length + self.snake2.length, MAX_SPEED_LENGTH)) / MAX_SPEED_LENGTH + MIN_FLAME

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
            pyxel.text(center("GAMEOVER", WINDOW_SIZE)  + randint(-1, 1), WINDOW_SIZE // 2 + randint(-1, 1), "GAMEOVER", 10)
            pyxel.text(center("GAMEOVER", WINDOW_SIZE), WINDOW_SIZE // 2, "GAMEOVER", 7)
            message = ["SCORE:", str(self.snake1.length), "x", str(self.snake2.length), ">>", str(self.snake1.length*self.snake2.length)]
            message_color = [7, 5, 7, 10, 7, 7]
            text_mc(center("".join(message), WINDOW_SIZE), WINDOW_SIZE // 4 * 3, message, message_color)
        else:
            # pyxel.text(center(str(self.flame), WINDOW_SIZE), WINDOW_SIZE//2, str(self.flame), 7)
            self.snake1.draw()
            self.snake2.draw()
            if App.apple:
                pyxel.rect(App.apple[0] * TILE_SIZE, App.apple[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE, 8)


App()