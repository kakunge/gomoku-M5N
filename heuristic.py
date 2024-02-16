import random

NONE = 0
WHITE = 1
BLACK = 2

def calcPlace(my_map, my_colour):
    values = heuristic(my_map, my_colour)
    max_value = max([max(row) for row in values])
    candidates = [(i, j) for i in range(15) for j in range(15) if values[i][j] == max_value]
    for i, j in candidates:
        if can_defend(my_map, i, j, my_colour):
            return i, j
    candidate = random.choice(candidates)
    return candidate[0], candidate[1]

def heuristic(my_map, my_colour):
    values = [[0 for _ in range(15)] for _ in range(15)]
    for i in range(15):
        for j in range(15):
            if my_map[i][j] == NONE:
                values[i][j] += evaluate_pattern_around(my_map, i, j, my_colour)
                values[i][j] += evaluate_pattern_around(my_map, i, j, 3 - my_colour)
    return values

def evaluate_pattern_around(my_map, i, j, my_colour):
    score = 0
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < 15 and 0 <= nj < 15 and my_map[ni][nj] == my_colour:
                score += evaluate_pattern(1)
            elif 0 <= ni < 15 and 0 <= nj < 15 and my_map[ni][nj] == 3 - my_colour:
                if count_consecutive(my_map, ni, nj, 3 - my_colour, di, dj) >= 4:
                    score += 1000
                elif count_consecutive(my_map, ni, nj, 3 - my_colour, di, dj) == 3:
                    score += 100
    return score

def can_win(my_map, i, j, my_colour):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            if count_consecutive(my_map, i, j, my_colour, di, dj) >= 4:
                return True
    return False

def can_defend(my_map, i, j, my_colour):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue
            if count_consecutive(my_map, i, j, 3 - my_colour, di, dj) >= 4:
                return True
    return False

def count_consecutive(my_map, i, j, my_colour, di, dj):
    count = 0
    ni, nj = i, j
    while 0 <= ni < 15 and 0 <= nj < 15 and my_map[ni][nj] == my_colour:
        count += 1
        ni += di
        nj += dj
    ni, nj = i - di, j - dj
    while 0 <= ni < 15 and 0 <= nj < 15 and my_map[ni][nj] == my_colour:
        count += 1
        ni -= di
        nj -= dj
    return count

def evaluate_pattern(count):
    if count >= 5:
        return 1000000
    elif count == 4:
        return 10000
    elif count == 3:
        return 1000
    elif count == 2:
        return 100
    elif count == 1:
        return 10
    else:
        return 0


