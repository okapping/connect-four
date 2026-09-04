import pyxel

from cell import Cell
from constants import *

SCENE_TITLE = 0
SCENE_SELECT = 1
SCENE_PLAY = 2

CELL_SIZE = 16
ROW_CNT = 6 #　縦6マス
COL_CNT = 7 #　横7マス

# PLAYER1, PLAYER2 = 0, 1

BASE_X = 24
BASE_Y = 32




class Game():
    def __init__(self):
        pyxel.init(width=160, height=140 ,title="コネクトフォー")
        # pyxel.init(width=128, height=112 ,title="rhythm action RPG")
        # pyxel.init(width=256, height=224 ,title="rhythm action RPG")
        self.font = pyxel.Font("assets/YokohamaDotsJPN.otf")#
        pyxel.mouse(True)
        pyxel.load("assets/asset.pyxres")
        
        self.scene = None

        self.cells = [[None]*COL_CNT for _ in range(ROW_CNT)]  # リストの初期化 6行7列のNone
        self.player = PLAYER1
        self.result = None
        
        self.debug = 1


        # 初期化
        self.change_scene(SCENE_TITLE)

        pyxel.run(self.update, self.draw)

    def change_scene(self, scene):
        self.scene = scene
    def is_click_inside_rect(self, x, y, w, h):
        """
        四角形の中をクリックしたかどうか判定する
        x, y: 左上の地点
        w, h: 幅と高さ（地点を含む）
        """
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (
                x < pyxel.mouse_x < x+w-1
                and y < pyxel.mouse_y < y+h-1
            ):
                return True
        return False

    def update_scene_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.change_scene(SCENE_SELECT)
    def update_scene_select(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.change_scene(SCENE_PLAY)
    
    def put_piece(self, col):
        """
        駒を置く
        col: 行のindex番号

        return: Bool
        """
        # 下から順番に確認する
        # for i, row in enumerate(reversed(self.cells)):
        for row in range(ROW_CNT - 1, -1, -1):
            # 空白セルに駒を置く
            if self.cells[row][col] is None:
                x = BASE_X + CELL_SIZE*col
                y = BASE_Y - CELL_SIZE
                tx = BASE_X + CELL_SIZE*col
                ty = BASE_Y + CELL_SIZE*row
                self.cells[row][col] = Cell(
                    self,
                    self.player,
                    x,
                    y,
                    tx,
                    ty
                )
                print(f"置けた on ({col}:{row})")
                return True
        return False
    
    def change_player(self):
        if self.player == PLAYER1:
            self.player = PLAYER2
        elif self.player == PLAYER2:
            self.player = PLAYER1

    def check_game_result(self):
        """
        ゲームに決着がついたかを確認する
        """
        cells = self.cells
        # 横の確認
        for row in range(ROW_CNT):
            for i in range(COL_CNT-3):
                if any(cells[row][i+j] is None for j in range(4)):
                    continue

                if all(cells[row][i+j].player == self.player for j in range(4)):
                    self.result = self.player
                    return True
        # 縦の確認
        for col in range(COL_CNT):
            for i in range(ROW_CNT-3):
                if any(cells[i+j][col] is None for j in range(4)):
                    continue

                if all(cells[i+j][col].player == self.player for j in range(4)):
                    self.result = self.player
                    return True

        # 斜め(＼)の確認
        # 斜め(／)の確認

    def main_game_logic(self, col):
        """
        ゲームのメインロジック！
        col: タップした行のindex番号
        """
        if self.result is not None:
            # 決着がついている場合は、ロジックは進まない
            return
        print(f"タップした col index: {col}")
        # コマを置く
        is_puted = self.put_piece(col)
        if not is_puted:
            return
        # 勝敗判定
        is_finished = self.check_game_result()
        # プレイヤー交代
        if is_finished:
            pass
        else:
            self.change_player()

    def update_scene_play(self):

        # size = 16
        for i in range(COL_CNT):
            x = BASE_X+CELL_SIZE*i
            y = BASE_Y
            w = CELL_SIZE
            h = CELL_SIZE*ROW_CNT
            if self.is_click_inside_rect(x, y, w, h):
                self.main_game_logic(i)

        for rows in self.cells:
            for cell in rows:
                if cell is None:
                    continue
                cell.update()

        # pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        # self.change_scene(SCENE_TITLE)

    def update(self):
        if self.scene == SCENE_TITLE:
            self.update_scene_title()
        elif self.scene == SCENE_SELECT:
            self.update_scene_select()
        elif self.scene == SCENE_PLAY:
            self.update_scene_play()

    def draw_scene_title(self):
        w = 140
        h = 60
        x = pyxel.width / 2 - w / 2
        # y = (pyxel.height / 2 - h / 2) - 20
        y = 20
        # pyxel.rect(x, y, w, h, 2)
        pyxel.blt(x, y, 1, 0, 0, w, h)

        s = "とっても面白い"
        x = pyxel.width / 2 - self.font.text_width(s) / 2
        y = 13
        pyxel.text(x, y, s, 7, self.font)

        s = "クリックでスタート！"
        x = pyxel.width / 2 - self.font.text_width(s) / 2
        y = 100
        pyxel.text(x, y, s, 7, self.font)
        if self.debug:
            pyxel.text(0, 0, "TITLE", 7)
    def draw_scene_select(self):
        if self.debug:
            pyxel.text(0, 0, "SELECT", 7)
    def draw_scene_play(self):
        if self.debug:
            pyxel.text(0, 0, "PLAY", 7)
            pyxel.text(0, 10, f"result: {self.result}", 7)
            

        for rows in self.cells:
            for cell in rows:
                if cell is None:
                    continue
                cell.draw()

        # 枠の枠
        # # 上の横
        # x = BASE_X-8
        # y = BASE_Y-8
        # for i in range((COL_CNT+1)*2):
        #     if i % 2 == 0:
        #         u, v = 24, 16
        #     else:
        #         u, v = 16, 16
        #     pyxel.blt(x, y, 0, u, v, 8, 8)
        #     x += 8
        # 枠
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                # 枠
                x = BASE_X + (CELL_SIZE*j)
                y = BASE_Y + (CELL_SIZE*i)
                pyxel.blt(x, y, 0, 16, 0, 16, 16, 10)
                # 空の場合はスキップ
                if cell is None:
                    continue
                
        
        # for i in range(6):
        #     for j in range(7):
    def draw(self):
        pyxel.cls(6)

        if self.scene == SCENE_TITLE:
            self.draw_scene_title()
        elif self.scene == SCENE_SELECT:
            self.draw_scene_select()
        elif self.scene == SCENE_PLAY:
            self.draw_scene_play()

        if self.debug:
            ...
            # pyxel.text(10, 10, f"cells: {len(self.cells[0])}", 0)

Game()