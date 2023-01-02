import pyxel
import random


MOVE_SPEED = 2
GOAL = [128, 128]
# キャラクターのクラスを作成
class Player:
    def __init__(self, x, y):
        # 表示位置の座標を示す変数
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0
        self.move_count = 0
    # ぬるりと移動する
    def move(self):
        self.x += self.dx
        self.y += self.dy


class Wall:
    def __init__(self):
        self.list = [
            [(32 * x) - 16, (32 * y) - 16] for x in range(1, 5) for y in range (1, 5)
        ]

        self.created = []

class App:
    def __init__(self):
        pyxel.init(144, 144)

        pyxel.load("maze.pyxres")

        # Playerクラスのインスタンスを生成、初期位置の座標を引数に渡す
        self.player = Player(0, 0)
        self.wall = Wall()
        self.create_walls()

    # 棒倒し法で迷路生成
    def create_walls(self):
        for wall in self.wall.list:
            self.random_walls(wall[0], wall[1])
        self.wall.list += self.wall.created

    def random_walls(self, x, y):
        # 1行目の壁以外では上方向に壁を生成しない
        if y == 16:
            n = random.randrange(0, 4)
        else:
            n = random.randrange(0, 3)

        dx, dy = 0, 0
        if n == 0:
            dx = 16
        elif n == 1:
            dx = -16
        elif n == 2:
            dy = 16
        else:
            dy = -16

        new_wall = [x + dx, y + dy]
        if new_wall in self.wall.created or new_wall == GOAL:
            # やり直し
            self.random_walls(x,y)
        else:
            # print(new_wall, n)
            self.wall.created.append(new_wall)



    def run(self):
        pyxel.run(self.update, self.draw)

    def update_move(self):
        # dx,dyの増減量を大きくするほど移動速度は上がる。
        # 移動量が0であれば、キー入力があるか判定する
        if self.player.move_count == 0:
            if pyxel.btnp(pyxel.KEY_LEFT) and [self.player.x - 16, self.player.y] not in self.wall.list and self.player.x - 16 >= 0:
                self.player.dx = -MOVE_SPEED
            elif pyxel.btnp(pyxel.KEY_RIGHT) and [self.player.x + 16, self.player.y] not in self.wall.list and self.player.x + 16 <= 128:
                self.player.dx = MOVE_SPEED
            elif pyxel.btnp(pyxel.KEY_UP) and [self.player.x, self.player.y - 16] not in self.wall.list and self.player.y - 16 >= 0:
                self.player.dy = -MOVE_SPEED
            elif pyxel.btnp(pyxel.KEY_DOWN) and [self.player.x, self.player.y + 16] not in self.wall.list and self.player.y + 16 <= 128:
                self.player.dy = MOVE_SPEED

            if self.player.dx != 0 or self.player.dy != 0:
                # move_count=16なら移動完了
                # 移動中はmove_countが0-16の間で増加中の状態である
                self.player.move_count = 16
                print([self.player.x, self.player.y])


        # 移動量が0でなければ、移動中の状態
        else:
            # playerを移動させ、移動量を1減らす
            self.player.move()
            self.player.move_count -= MOVE_SPEED

            # 移動量が0になったら移動終了、x,yの変化量をリセットする
            if self.player.move_count == 0:
                self.player.dx = 0
                self.player.dy = 0

    def update(self):
        self.update_move()

    def draw(self):
        # 背景の描画：(x, y, tm, u, v, w, h, colkey)
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 144, 144, 0)

        # playerの変数x,yを使用して描画
        pyxel.blt(self.player.x, self.player.y, 0, 0, 0, 16, 16, 0)

        for wall in self.wall.list:
            pyxel.blt(wall[0],wall[1], 0, 48, 0, 16, 16, 0)

        if [self.player.x, self.player.y] == GOAL:
            pyxel.rect(0, 0, 144, 16, 5)
            pyxel.text(64, 5, "GOAL!", 7)

App().run()