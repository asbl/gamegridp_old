W = 119
S = 115
A = 97
D = 100
SPACE = 32
UP = 273
DOWN = 274
LEFT = 276
RIGHT = 275
Q = 113
E = 101
Y = 122
X = 120
C = 99


def key_pressed_to_key(key_pressed_list: list):
    keys = []
    for index, item in enumerate(key_pressed_list):
        if item:
            if index == W:
                keys.append("W")
            if index == S:
                keys.append("S")
            if index == A:
                keys.append("A")
            if index == D:
                keys.append("D")
            if index == UP:
                keys.append("UP")
            if index == DOWN:
                keys.append("DOWN")
            if index == LEFT:
                keys.append("LEFT")
            if index == RIGHT:
                keys.append("RIGHT")
            if index == Q:
                keys.append("Q")
            if index == E:
                keys.append("E")
            if index == Y:
                keys.append("Y")
            if index == X:
                keys.append("X")
            if index == C:
                keys.append("C")
    return keys
