from core.utils.utils import Gfx



def createImgSprite(idx, pos, size, spriteBox):
    params ={
        "filePath" : "resources/image01.png",
        "size" : size,
        "position" : pos,
        "filterColor": (255, 255, 255, 0),
        "spriteBox" : spriteBox,
        "startIndex" : idx,
        "endIndex" : idx
    }
    img = Gfx.create_animated(params)
    return img


def getImagesAtPos(imgs, pos):
    ans = []
    for I in imgs:
        if I.center_x == pos[0] and I.center_y == pos[1]:
            ans.append(I)
    return ans