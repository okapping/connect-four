import pyxel
import random
from constants import *

class Piece:
    def __init__(self, game, player, x, y, tx, ty):
        self.game = game
        self.player = player
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty

        self.aligned = False
        self.sparkles = []
    
    def update_effect(self):
        if not self.aligned:
            return

        if pyxel.rndi(1, 10) == 1:
            angle = pyxel.rndi(0, 360)
            distance = pyxel.rndi(3, 8)
            sparkle = {
                "x": int(self.x+8 + pyxel.cos(angle) * distance),
                "y": int(self.y+8 + pyxel.sin(angle) * distance),
                "life": pyxel.rndi(8, 20),
                "size": random.choice([1, 1, 1, 1, 2]),
            }
            self.sparkles.append(sparkle)
    
        # キラキラの寿命を減らす
        for sparkle in self.sparkles:
            sparkle["life"] -= 1

        # 寿命がなくなったキラキラを削除
        self.sparkles = [
            sparkle
            for sparkle in self.sparkles
            if sparkle["life"] > 0
        ]

    def update(self):
        self.x = self.tx
        self.y = min(self.y + 12, self.ty)

        self.update_effect()

    def draw_aligned_effect(self):
        if not self.aligned:
            return

        for sparkle in self.sparkles:
            x = sparkle["x"]
            y = sparkle["y"]
            life = sparkle["life"]
            size = sparkle["size"]

            # 残り時間に応じて色を変える
            color = 7 if life % 4 < 2 else 10

            # 十字型の輝き
            pyxel.line(x - size, y, x + size, y, color)
            pyxel.line(x, y - size, x, y + size, color)

        
    def draw(self):
        if self.player == PLAYER1:
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 0)
        elif self.player == PLAYER2:
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16, 0)
        
        # pyxel.text(self.x+8, self.y+8, f"{self.aligned}", 7)
        # pyxel.text(self.x+8, self.y+8, f"{len(self.sparkles)}", 7)

