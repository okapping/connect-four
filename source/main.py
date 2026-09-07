import pyxel
import random

from piece import Piece
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

MARGIN = 4

RELOAD_BTN = (16, 16)


class Game():
    def __init__(self):
        pyxel.init(width=160, height=140 ,title="コネクトフォー")
        # pyxel.init(width=128, height=112 ,title="rhythm action RPG")
        # pyxel.init(width=256, height=224 ,title="rhythm action RPG")
        self.font = pyxel.Font("assets/YokohamaDotsJPN.otf")#
        pyxel.mouse(True)
        pyxel.load("assets/asset.pyxres")
        
        self.scene = None

        # タイトル画面
        self.falling_pieces = []
        self.msg_y = 100
        self.msg_dy = -0.3
        self.title_clicked = None
        self.title_alpha = 1
        self.bg_left_x = 0
        self.bg_right_x = pyxel.width // 2
        # プレイ画面
        self.cells = [[None]*COL_CNT for _ in range(ROW_CNT)]  # リストの初期化 6行7列のNone
        self.player = PLAYER1
        self.result = None
        self.animation_pieces = []

        self.reload_btn_pos = (pyxel.width-(16+MARGIN), MARGIN, 16, 16)
        
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

    def update_title_effect(self):
        ##### 背景のコマ
        # コマを追加
        if pyxel.frame_count / 10 % 2 == 0:
            self.falling_pieces.append(
                (
                    16 * pyxel.rndi(0, pyxel.width // 16 // 2 - 1),
                    -16,
                    random.choice([PLAYER1, PLAYER2]),
                    pyxel.rndi(0, 1)
                )
            )
        # 下へ落下させる
        for i, piece in enumerate(self.falling_pieces):
            x, y, player, side = piece
            self.falling_pieces[i] = (x, y+3, player, side)
        
        self.falling_pieces = [piece for piece in self.falling_pieces if piece[1] < pyxel.height]
        
        ##### クリックでスタートのバウンズ
        self.msg_y += self.msg_dy
        self.msg_dy += 0.02
        if self.msg_y > 100:
            # self.msg_y = 100
            self.msg_dy = -0.3


    def update_scene_title(self):
        now = pyxel.frame_count
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.title_clicked = now
            # self.change_scene(SCENE_SELECT)
        
        if self.title_clicked is not None:
            # タイトルをフェードアウト
            self.title_alpha -= 0.04
            # 背景を扉のようにあける
            if now > self.title_clicked + 30:
                self.bg_left_x = max(self.bg_left_x-5, -pyxel.width // 2)
                self.bg_right_x = min(self.bg_right_x+5, pyxel.width)
            # シーン変更
            if now > self.title_clicked + 60:
                self.change_scene(SCENE_SELECT)
        
        self.update_title_effect()

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
                self.cells[row][col] = Piece(
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
        終了した場合Trueを返す。
        結果はself.resultを確認する。
        """
        cells = self.cells
        # 横の確認
        for row in range(ROW_CNT):
            for col in range(COL_CNT-3):
                if any(cells[row][col+i] is None for i in range(4)):
                    continue

                if all(cells[row][col+i].player == self.player for i in range(4)):
                    for i in range(4):
                        cells[row][col+i].aligned = True
                    self.result = self.player
                    return True
        # 縦の確認
        for col in range(COL_CNT):
            for row in range(ROW_CNT-3):
                if any(cells[row+i][col] is None for i in range(4)):
                    continue

                if all(cells[row+i][col].player == self.player for i in range(4)):
                    for i in range(4):
                        cells[row+i][col].aligned = True
                    self.result = self.player
                    return True

        # 斜め(＼)の確認
        for row in range(ROW_CNT-3):
            for col in range(COL_CNT-3):
                if any(cells[row+i][col+i] is None for i in range(4)):
                    continue

                if all(cells[row+i][col+i].player == self.player for i in range(4)):
                    for i in range(4):
                        cells[row+i][col+i].aligned = True
                    self.result = self.player
                    return True

        # 斜め(／)の確認
        for row in range(ROW_CNT-3):
            for col in range(COL_CNT-3):
                if any(cells[row+(3-i)][col+i] is None for i in range(4)):
                    continue

                if all(cells[row+(3-i)][col+i].player == self.player for i in range(4)):
                    for i in range(4):
                        cells[row+(3-i)][col+i].aligned = True
                    self.result = self.player
                    return True
        
        if all(all(cell is not None for cell in row) for row in self.cells ):
            self.result = DRAW
            return True
        
        return False

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
        if is_finished:
            pass
        else:
            # プレイヤー交代
            self.change_player()
    def game_init(self):
        """
        ゲームの初期化
        """
        self.cells = [[None]*COL_CNT for _ in range(ROW_CNT)]  # リストの初期化 6行7列のNone
        self.player = PLAYER1
        self.result = None

    def update_pieces_fall_animation(self):
        """
        リロード後にコマが落ちるアニメーション
        """
        for row in range(len(self.animation_pieces)):
            for col in range(len(self.animation_pieces[row])):
                if self.animation_pieces[row][col] is None:
                    continue
                self.animation_pieces[row][col].y += 6
                if self.animation_pieces[row][col].y > pyxel.height:
                    self.animation_pieces[row][col] = None

    def update_scene_play(self):
        # リロードボタンをクリックした場合
        if self.is_click_inside_rect(*self.reload_btn_pos):
            self.animation_pieces = self.cells.copy()
            self.game_init()
        
        # 
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

        self.update_pieces_fall_animation()


    def update(self):
        if self.scene == SCENE_TITLE:
            self.update_scene_title()
        elif self.scene == SCENE_SELECT:
            self.update_scene_select()
        elif self.scene == SCENE_PLAY:
            self.update_scene_play()

    def draw_scene_title(self):
        pyxel.cls(0)
        # 落ちてくるコマ
        for piece in self.falling_pieces:
            x, y, player, side = piece
            if player == PLAYER1:
                u, v = 32, 0
            elif player == PLAYER2:
                u, v = 48, 0
            if side == 0:
                x += self.bg_left_x
            elif side == 1:
                x += self.bg_right_x
            pyxel.blt(x, y, 0, u, v, 16, 16, 0)
        # 背景
        # 左側
        for i in range(pyxel.width // 16 // 2):
            for j in range(pyxel.ceil(pyxel.height / 16)):
                pyxel.blt(self.bg_left_x+16*i, 16*j, 0, 0, 16, 16, 16, 0)
        
        # 右側
        for i in range(pyxel.width // 16 // 2):
            for j in range(pyxel.ceil(pyxel.height / 16)):
                pyxel.blt(self.bg_right_x+16*i, 16*j, 0, 0, 16, 16, 16, 0)

        pyxel.dither(self.title_alpha)
        w = 140
        h = 60
        x = pyxel.width / 2 - w / 2
        # y = (pyxel.height / 2 - h / 2) - 20
        y = 20
        # pyxel.rect(x, y, w, h, 2)
        pyxel.blt(x, y, 1, 0, 0, w, h, 2)

        s = "おとしてそろえて"
        x = pyxel.width / 2 - self.font.text_width(s) / 2
        y = 13
        for i in range(1, -1, -1):
            pyxel.text(x+i, y+i, s, 0 if i else 7, self.font)
        # pyxel.text(x, y, s, 7, self.font)

        s = "クリックでスタート！"
        x = pyxel.width / 2 - self.font.text_width(s) / 2
        # y = 100
        for i in range(1, -1, -1):
            pyxel.text(x+i, self.msg_y+i, s, 0 if i else 7, self.font)
        
        pyxel.dither(1)

        if self.debug:
            pyxel.text(0, 0, "TITLE", 7)
            # pyxel.text(0, 10, f"{len(self.falling_pieces)}", 7)
    def draw_scene_select(self):
        if self.debug:
            pyxel.text(0, 0, "SELECT", 7)
    def draw_scene_play(self):
        if self.debug:
            pyxel.text(0, 0, "PLAY", 7)
            pyxel.text(0, 10, f"result: {self.result}", 7)
            
        # リロードボタン
        x, y, w, h = self.reload_btn_pos
        pyxel.blt(x, y, 0, *RELOAD_BTN, w, h, 0)

        # 落ちていくコマ一覧
        for row in self.animation_pieces:
            for piece in row:
                if piece is None:
                    continue
                piece.draw()

        # コマ一覧
        for row in self.cells:
            for cell in row:
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

        
        # コマのエフェクト一覧
        for row in self.cells:
            for cell in row:
                if cell is None:
                    continue
                cell.draw_aligned_effect()
                
        
        # for i in range(6):
        #     for j in range(7):
    def draw(self):
        pyxel.cls(0)

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