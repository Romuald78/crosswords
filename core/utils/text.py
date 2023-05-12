from core.utils.utils import Gfx

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA += ALPHA.lower()
ALPHA += "0123456789-- "
ALPHA += ".,;:@#'\"/?<>"
ALPHA += "%&*()-$"

def createCharSprite(letter, pos, size):
    idx = ALPHA.index(letter)
    params ={
        "filePath" : "resources/letters.png",
        "size" : size,
        "position" : pos,
        "filterColor": (255, 255, 255, 128),
        "spriteBox" : (13,7,74,80),
        "startIndex" : idx,
        "endIndex" : idx
    }
    letter = Gfx.create_animated(params)
    return letter

# pos is the pos of the top left letter
# size1 is the size of 1 letter
def createWordSprites(word, pos, indexes, size1, vertical=False):
    letters = []
    dx = 1
    dy = 0
    if vertical:
        dy = 1
        dx = 0
    x = pos[0]
    y = pos[1]
    for w in word:
        # print(f"    Lettre {w}")
        letter = createCharSprite(w, (x, y), (size1[0] * 2, size1[1] * 2))
        letter.dispSpr = 0
        # print(f"    store indexes : {indexes}")
        letter.indexes = indexes

        letters.append(letter)
        x += dx * size1[0]
        y -= dy * size1[1]
        indexes = (indexes[0]+dx, indexes[1]+dy)
    return letters

def getLettersAtPos(letters, pos):
    ans = []
    for L in letters:
        if (L.center_x, L.center_y) == pos:
            ans.append(L)
    return ans


def getLettersAtIdx(letters, indexes):
    ans = []
    for L in letters:
        if L.indexes == indexes:
            ans.append(L)
    #print(ans)
    return ans

def getLettersFromWord(word, i, j, vertical, all_letters):
    out = []
    L = len(word)
    indexes = (i, j)
    dx = 1
    dy = 0
    if vertical:
        dy = dx
        dx = 0
    #print("-----------------------------------")
    for loop in range(L):
        idx = (indexes[0] + dx * loop, indexes[1] + dy * loop)
        letter = getLettersAtIdx(all_letters, idx)
        out += letter
    return out

def displayWord(word, i, j, vertical, all_letters, newState):
    out = getLettersFromWord(word, i, j, vertical, all_letters)
    for l in out:
        if newState == l.dispSpr + 1:
            l.dispSpr = newState

def checkCompleteWord(word, i, j, vertical, all_letters):
    out = getLettersFromWord(word, i, j, vertical, all_letters)
    for l in out:
        if l.dispSpr == 0:
            return False
    return True

def all_letters_found(letters):
    for l in letters:
        if l.dispSpr != 2:
            return False
    return True