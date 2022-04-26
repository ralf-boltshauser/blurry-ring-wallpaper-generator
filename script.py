
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import imageio

COLOR = [31, 29, 28]
BACKGROUND_COLOR = (117, 95, 79)


def generateCircleMask(face, x, y, w, h, r):
    SqDist = r**2 * r
    return (h/2 - y) ** 2 + (w/2 - x) ** 2 < SqDist


def drawCircle(face, oldface, x, y, w, h, r, t):
    mask = generateCircleMask(oldface, x, y, w, h, r)
    face[mask] = COLOR
    restoremask = generateCircleMask(oldface, x, y, w, h, r-t)
    face[restoremask] = oldface[restoremask]
    return face


def drawCircles(face, oldface, x, y, w, h, r, t, b, amount):

    for i in range(0, amount):
        face = drawCircle(face, oldface, x, y, w, h, r - (t * i * b), t)
    return face


# get user input
smallMatch = input("Small match? (y/n) ")
# convert to bool
smallMatch = (smallMatch == 'y')

face = imageio.imread('images/8.jpg')
face[10:13, 20:23]

lx, ly, _ = face.shape
X, Y = np.ogrid[0:lx, 0:ly]
oldface = face.copy()
face = drawCircles(face, oldface, X, Y, lx, ly, 50, 0.5, 3, 50)
# mask = X < Y
# face[mask] = face[mask] * (1, 2, 0.5)


def f(lists):
    arr = np.array(lists)
    return len(arr.shape)


def surroundingIsCircled(face, x, y):
    if (np.array_equal(face[x - 1][y - 1], COLOR)):
        return True
    if (np.array_equal(face[x - 1][y], COLOR)):
        return True
    if (np.array_equal(face[x - 1][y + 1], COLOR)):
        return True
    if (np.array_equal(face[x][y - 1], COLOR)):
        return True
    if (np.array_equal(face[x][y + 1], COLOR)):
        return True
    if (np.array_equal(face[x + 1][y - 1], COLOR)):
        return True
    if (np.array_equal(face[x + 1][y], COLOR)):
        return True
    if (np.array_equal(face[x + 1][y + 1], COLOR)):
        return True
    return False


# initialize white image with face size
finalFace = np.ones((lx, ly, 3), dtype=np.uint8) * BACKGROUND_COLOR

for x in range(0, lx):
    for y in range(0, ly):
        if not np.array_equal(face[x][y], oldface[x][y]):
            finalFace[x][y] = face[x][y]
        try:
            if (smallMatch):
                if np.array_equal(oldface[x][y], [0, 0, 0]) and np.array_equal(face[x][y], [0, 0, 0]) and (np.array_equal(face[x - 1][y - 1], COLOR) or np.array_equal(face[x + 1][y - 1], COLOR)):
                    finalFace[x][y] = COLOR
            else:
                if np.array_equal(oldface[x][y], [0, 0, 0]) and np.array_equal(face[x][y], [0, 0, 0]) and surroundingIsCircled(face, x, y):
                    finalFace[x][y] = COLOR
        except:
            continue

plt.figure(figsize=(5, 5))
plt.axes([0, 0, 1, 1])
plt.imshow(finalFace, cmap=plt.cm.gray)
plt.axis('off')

plt.show()
