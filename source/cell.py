import pyxel
from constants import *

class Cell:
    def __init__(self, game, player, x, y, tx, ty):
        self.game = game
        self.player = player
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty
    
    def update(self):


        self.x = self.tx
        self.y = min(self.y + 12, self.ty)

    def draw(self):
        if self.player == PLAYER1:
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 0)
        elif self.player == PLAYER2:
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16, 0)

