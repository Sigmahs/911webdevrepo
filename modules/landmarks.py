
def firstmodify(left, right, up, bottom, margin_perc=20):
    """
    This function is to make a square images based on the facemark + margin.

    Args:
        left(int): the left border of the image.
        right(int): the right border of the image.
        up(int): the bottom border of the image.
        bottom(int): the upper border of the image.
        margin_perc(int): the percentage, change it to control the margin width

    Returns:
        int: the new border of the image.

    """
    if (right-left)>=(bottom-up):
        margin = int((right-left)*margin_perc/100)
        diff = (right-left)-(bottom-up)
        if diff%2 == 0:
            left = int(left-margin)
            right = int(right+margin)
            up = int(up-margin-diff)
            bottom = int(bottom+margin)

        else:
            left = int(left-margin)
            right = int(right+margin)
            up = int(up-margin-diff)
            bottom = int(bottom+margin)
    else:
        margin = int((bottom-up)*margin_perc/100)
        diff = (bottom-up)-(right-left)
        if diff%2 == 0:
            left = int(left-margin-diff/2)
            right = int(right+margin+diff/2)
            up = int(up-margin)
            bottom = int(bottom+margin)
        else:
            left = int(left-margin-(diff/2+0.5))
            right = int(right+margin+(diff/2-0.5))
            up = int(up-margin)
            bottom = int(bottom+margin)

    return left, right, up, bottom



def ifoverborder(left, right, up, bottom, width, height):
    if left < 0:
        right = right + (0-left)
        left = 0
        if right > width:
            right = width
    if right > width:
        left = left - (right-width)
        right = width
        if left < 0:
            left = 0
    if up < 0:
        bottom = bottom + (0-up)
        up = 0
        if bottom > height:
            bottom = height
    if bottom > height:
        up = up - (bottom - height)
        bottom = height
        if up < 0:
            up = 0
    #print(left, right, up, bottom, width, height)
    return left, right, up, bottom

def finalmodify(left, right, up, bottom):
    #print(left, right, up, bottom)
    if right - left < bottom - up:
        diff = (bottom-up)-(right-left)
        if diff%2 == 0:
            up = int(up+diff/2)
            bottom = int(bottom-diff/2)
        else:
            up = int(up+diff/2-0.5)
            bottom = int(bottom-diff/2-0.5)
    else:
        diff = (right-left)-(bottom-up)
        if diff%2 == 0:
            left = int(left+diff/2)
            right = int(right-diff/2)
        else:
            left = int(left+diff/2+0.5)
            right = int(right-diff/2+0.5)
    #print(left, right, up, bottom)
    return left, right, up, bottom

