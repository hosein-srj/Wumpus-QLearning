import numpy as np
from graphics import *

rows = 5
cols = 5
Win_State = (4, 4)
Lose_States = [(2, 3), (3, 3), (4, 3)]
Start = (1, 1)
iteration = 300
df = 0.9
lnd = 1
eps = 0.5


def reach_terminal(point, rewards):
    x = point[0]
    y = point[1]
    if rewards[x][y] == -1:
        return True
    return False


def find_action(point, epsilon, Q_ar):
    x = point[0]
    y = point[1]
    f_a = [Q_ar[x][y][0], Q_ar[x][y][1], Q_ar[x][y][2], Q_ar[x][y][3]]
    if x == 0:
        f_a[3] = -100
    if x == 4:
        f_a[1] = -100
    if y == 0:
        f_a[2] = -100
    if y == 4:
        f_a[0] = -100
    if np.random.random() < epsilon:
        # return np.argmax(Q_ar[point[0], point[1]])
        return np.argmax(np.array(f_a))
    else:
        r = np.random.randint(4)
        while f_a[r] == -100:
            r = np.random.randint(4)
        return r
        # return np.argmax(np.array(f_a))


def find_s(action_s, point):
    x = point[0]
    y = point[1]
    s = (x, y)
    if (action_s == 0) and y < 4:
        s = (x, y + 1)
    elif (action_s == 1) and x < 4:
        s = (x + 1, y)
    elif (action_s == 2) and y > 0:
        s = (x, y - 1)
    elif (action_s == 3) and (x > 0):
        s = (x - 1, y)

    return s


def find_q_matris(it):
    reward = [[-1 for i in range(cols)] for j in range(rows)]
    for i in range(0, rows):
        for j in range(0, cols):
            if (i, j) == Win_State:
                reward[i][j] = 100
            if (i, j) in Lose_States:
                reward[i][j] = -100

    Q = [[[0 for i in range(4)] for j in range(cols)] for k in range(rows)]
    Q = np.array(Q)

    for repeat in range(it):
        cur = Start
        while reach_terminal(cur, reward):
            action = find_action(cur, eps, Q)
            new_s = find_s(action, cur)
            Q[cur[0]][cur[1]][action] = reward[new_s[0]][new_s[1]] + df * np.max(Q[new_s[0], new_s[1]])
            cur = new_s
    return Q


def find_cord(point):
    for i in range(5):
        for j in range(5):
            if (point.x > 100 + i * 75 + 5) and (point.x < 175 + i * 75) and (point.y > 175 + j * 75 + 5) and (
                    point.y < 250 + j * 75):
                return i, j

    return -1, -1


def compute_shortest_path(Q_matris, st):
    c = Start
    shortest_path = []
    while c != Win_State:
        x = np.argmax(q_mat[c[0], c[1]])
        if x == 0:
            shortest_path.append("R")
            c = (c[0], c[1] + 1)
        elif x == 1:
            shortest_path.append("D")
            c = (c[0] + 1, c[1])
        elif x == 2:
            shortest_path.append("L")
            c = (c[0], c[1] - 1)
        elif x == 3:
            shortest_path.append("U")
            c = (c[0] - 1, c[1])

    return shortest_path


if __name__ == "__main__":
    win = GraphWin('Q-Learning', 900, 600)

    clicked = 0
    rects = []
    for i in range(5):
        for j in range(5):
            rect = Rectangle(Point(100 + i * 75 + 5, 175 + j * 75 + 5), Point(175 + i * 75, 250 + j * 75))
            rects.append(rect)
            rect.draw(win)

    while clicked != 5:
        point = win.getMouse()
        i, j = find_cord(point)
        if (i >= 0) and (i <= 4) and (j >= 0) and (j <= 5):
            if clicked == 0:
                # goal
                rects[i * 5 + j].setFill('Green')
                Win_State = (j, i)
            if clicked == 1:
                # Start
                rects[i * 5 + j].setFill('Blue')
                Start = (j, i)
            if clicked == 2 or clicked == 3:
                # Hole
                Lose_States[clicked - 2] = (j, i)
                rects[i * 5 + j].setFill('Red')
            if clicked == 4:
                # Wall
                Lose_States[clicked - 2] = (j, i)
                rects[i * 5 + j].setFill('Black')
            clicked = clicked + 1

    q_mat = find_q_matris(700)

    shortest_path = compute_shortest_path(q_mat, Start)

    label = Text(Point(660, 20), 'Right\tDown\tLeft\tUp')
    label.setTextColor('red')
    label.draw(win)
    for i in range(5):
        for j in range(5):
            some = Text(Point(700, 50 + 20 * (i * 5 + j)),
                        str(q_mat[i][j][0]) + '\t' + str(q_mat[i][j][1]) + '\t' + str(q_mat[i][j][2])
                        + '\t' + str(q_mat[i][j][3]) + '\t' + '[' + str(i) + ',' + str(j) + ']')
            some.draw(win)
    path = shortest_path[0]
    for l in range(1, len(shortest_path)):
        path = path + " => " + shortest_path[l]

    pa = Text(Point(250, 100), 'The Shortest Path is: '+path)
    pa.setTextColor('Blue')
    pa.draw(win)
    while True:
        win.getMouse()

# print("Right \t Down \t Left \t Up")
# for i in range(rows):
#     for j in range(cols):
#         print("[" + str(i) + "," + str(j) + "]  " + str(q_mat[i][j][0]) + "\t" + str(q_mat[i][j][1]) + "\t" + str(
#             q_mat[i][j][2]) + "\t" + str(q_mat[i][j][3]))
