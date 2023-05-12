import random

import arcade

from core.utils.image import createImgSprite, getImagesAtPos
from core.utils.text import *
from core.utils.utils import Gfx



class Page1Home():

    GRID_W    = 11
    GRID_H    = 7
    CHAR_SIZE = 125

    WORDS =[
        ("ROMUALD", 0, 1, False),
        ("GRIGNON", 0, 0, True),
        ("NOEL", 0, 4, False),
        ("LIT", 3, 4, True),
        ("MUSE", 2, 1, True),
        ("DIRECT", 6, 1, True),
        ("ROYAL", 6, 3, False),
    ]

    def __init__(self, w, h, window: arcade.Window, process=None):
        super().__init__()
        self.window = window
        self.W = w
        self.H = h
        self.process = process

    def refresh(self):
        self.setup()

    def setup(self, config=None):
        params = {
            "filePath": "resources/unesco.jpg",
            "position": (self.W/2, self.H/2),
            "filterColor" : (255,255,255,255),
            "size":(max(self.W,self.H), max(self.W,self.H)),
        }

        self.background = Gfx.create_fixed(params)

        self.xRef = (self.W - self.CHAR_SIZE * self.GRID_W) / 2 + self.CHAR_SIZE / 2
        self.yRef = (self.H + self.CHAR_SIZE * self.GRID_H) / 2 - self.CHAR_SIZE / 2

        self.all_letters = []
        self.all_images = []
        for w in self.WORDS:
            # print(f">>>>> Mot {w}")
            pos  = (self.xRef + w[1]*self.CHAR_SIZE, self.yRef - w[2]*self.CHAR_SIZE)
            size = (self.CHAR_SIZE, self.CHAR_SIZE)
            letters = createWordSprites(w[0], pos, (w[1],w[2]), size, w[3])

            self.all_letters += letters

        for l in self.all_letters:
            size = (self.CHAR_SIZE, self.CHAR_SIZE)
            pos  = (l.center_x, l.center_y)
            x = (l.center_x - self.xRef)/self.CHAR_SIZE
            y = (self.yRef - l.center_y)/self.CHAR_SIZE
            div = min(835//self.GRID_W, 549//self.GRID_H)
            spbox = (self.GRID_W, self.GRID_H, div, div)
            img = createImgSprite(x + y * self.GRID_W, pos, size, spbox)
            self.all_images.append(img)

        w = self.W * 0.95
        h = self.H * 0.95
        params = {
            "filePath": "resources/image01.png",
            "size": ( w, h ),
            "position": ( self.W/2, self.H/2 ),
            "filterColor": (255, 255, 255, 255),
        }
        self.picture = Gfx.create_fixed(params)
        self.picture.final_scale = self.picture.scale
        self.picture.scale = 0.01

        self.started = False

    def update(self, deltaTime):
        # check if a word is finished
        for i in range(len(self.WORDS)):
            res = checkCompleteWord(self.WORDS[i][0], self.WORDS[i][1], self.WORDS[i][2], self.WORDS[i][3], self.all_letters)
            if res:
                displayWord(self.WORDS[i][0], self.WORDS[i][1], self.WORDS[i][2], self.WORDS[i][3], self.all_letters, 2)


    def draw(self):
        self.background.draw()

        if all_letters_found(self.all_letters):
            self.picture.scale = min(self.picture.scale*1.1, self.picture.final_scale)
            self.picture.draw()
        elif self.started:
            for letter in self.all_letters:
                if letter.dispSpr >= 2:
                    img = getImagesAtPos(self.all_images, (letter.center_x, letter.center_y))
                    img[0].color = (255,255,255,min(img[0].alpha+5,255))
                    img[0].draw()

                    # check if this is a multi letter (and continue to display it with transparency
                    siblings  = getLettersAtPos(self.all_letters, (letter.center_x, letter.center_y))
                    res = 1
                    if len(siblings) > 1:
                        letter.color = (255,255,255,128)
                        # Check if the 2 words for this letter are completely visible
                        # in this case we do not have to display the letter
                        adjacent = []
                        adjacent += getLettersAtIdx(self.all_letters, (siblings[0].indexes[0] - 1, siblings[0].indexes[1]))
                        adjacent += getLettersAtIdx(self.all_letters, (siblings[0].indexes[0] + 1, siblings[0].indexes[1]))
                        adjacent += getLettersAtIdx(self.all_letters, (siblings[0].indexes[0], siblings[0].indexes[1] - 1))
                        adjacent += getLettersAtIdx(self.all_letters, (siblings[0].indexes[0], siblings[0].indexes[1] + 1))
                        show = False
                        for adj in adjacent:
                            if adj.dispSpr < 2:
                                show = True
                        if show:
                            letter.draw()
                else:
                    size = max(letter.width/2, letter.height/2)
                    arcade.draw_rectangle_filled(letter.center_x, letter.center_y,
                                                 size, size,
                                                 (200,200,255,255))
                    arcade.draw_rectangle_outline(letter.center_x, letter.center_y,
                                                 size, size,
                                                 (0,0,0,255))
                    if letter.dispSpr == 1:
                        letter.color = (255,255,255,255)
                        letter.draw()

    def onMouseButtonEvent(self, x, y, buttonNum, isPressed):
        for letter in self.all_letters:
            size = max(letter.width / 2, letter.height / 2) / 2
            x0   = letter.center_x - size
            y0   = letter.center_y - size
            x1   = letter.center_x + size
            y1   = letter.center_y + size
            if x0 <= x <= x1 and y0 <= y <= y1:
                letter.dispSpr = 1

    def onKeyEvent(self, key, isPressed):
        if key == arcade.key.SPACE and isPressed:
            self.started = True