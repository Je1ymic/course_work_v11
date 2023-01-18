from tkinter import *
import random
import time
import copy
from tkinter import messagebox

MainWindow = Tk()
MainWindow.title('Checkers')
Square = Canvas(MainWindow, width=780, height=780, bg='#545454')
Square.pack()

n2_sp = ()
ur = 1
k_rez = 0
o_rez = 0
poz1_x = -1


HOD = 0

peshki = [PhotoImage(file="resources/white.png"), PhotoImage(file="resources/white_king.png"), PhotoImage(file="resources/black.png"), PhotoImage(file="resources/black_king.png")]


def draw_viv(x1, y1, x2, y2):
    global peshki
    global Board
    global choosedFigure, isGoodFigure
    Square.delete('all')

    for i in range(0, 144):
        if i % 2 == 0:
            dy = i // 12
            dx = i % 12 + dy % 2
            Square.create_rectangle(dx * 65, dy * 65, dx * 65 + 65, dy * 65 + 65, fill="white")

    for y in range(12):
        for x in range(12):
            figura = Board[y][x]
            if figura:
                if (x1, y1) != (x, y):
                    Square.create_image(x * 65, y * 65, anchor=NW, image=peshki[figura - 1])

    figura = Board[y1][x1]
    if figura:
        Square.create_image(x1 * 65, y1 * 65, anchor=NW, image=peshki[figura - 1], tag='choosed')
    isGoodFigure = Square.create_rectangle(0, 0, 0, 0, outline="#adff7a", width=5)
    choosedFigure = Square.create_rectangle(0, 0, 0, 0, outline="#f4ff75", width=5)
    znak_x = 1 if x1 < x2 else -1
    znak_y = 1 if y1 < y2 else -1
    kletok = abs(x1 - x2)
    for ii in range(10):
        Square.move('choosed', 0.1 * 65 * znak_x * kletok, 0.1 * 65 * znak_y * kletok)
        Square.update()
        time.sleep(0.001)


def start_game():
    global Board
    Board = [
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
        [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    ]


def HighlightCell(event):
    global HOD
    cellX, cellY = (event.x) // 65, (event.y) // 65
    goodCell = False
    if 0 <= cellX < 12 and 0 <= cellY < 12 and HOD == 0:
        if Board[cellY][cellX] == 1:
            Square.coords(isGoodFigure, cellX * 65 + 3, cellY * 65 + 3, cellX * 65 + 62, cellY * 65 + 62)
            goodCell = True
    if not goodCell:
        Square.coords(isGoodFigure, -5, -5, -5, -5)


def ClickHandler(event):
    global poz1_x, poz1_y, poz2_x, poz2_y
    global HOD
    x, y = (event.x) // 65, (event.y) // 65
    if Board[y][x] == 1 or Board[y][x] == 2 and HOD == 0:
        Square.coords(choosedFigure, x * 65 + 3, y * 65 + 3, x * 65 + 62, y * 65 + 62)
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:
            poz2_x, poz2_y = x, y
            if HOD == 0:
                PlayerTurn()
                if HOD == 1:
                    time.sleep(0.5)
                    CompTurn()
            poz1_x = -1
            Square.coords(choosedFigure, -5, -5, -5, -5)


def GameOver(s, debug=""):
    global HOD
    reasons = [
        'Вы проиграли!\nНажми "Да" что бы начать заново.',
        'Вы выиграли!\nНажми "Да" что бы начать заново.',
        'Ходов больше нет. Вы выиграли\nНажми "Да" что бы начать заново.',
        'У соперника больше нет ходов. Вы проиграли\nНажми "Да" что бы начать заново.'
    ]
    isNewGame = messagebox.askyesno(title="Игра окончена", message=reasons[s - 1] + debug, icon='info')

    if isNewGame:
        start_game()
        draw_viv(-1, -1, -1, -1)
        HOD = 0


def CompTurn():
    global n2_sp
    global HOD
    HOD = 1
    CheckCompTurn(1, (), [])
    if n2_sp:
        kh = len(n2_sp)
        th = random.randint(0, kh - 1)
        dh = len(n2_sp[th])
        for h in n2_sp:
            h = h
        for i in range(dh - 1):
            turns_list = Turn(1, n2_sp[th][i][0], n2_sp[th][i][1], n2_sp[th][1 + i][0], n2_sp[th][1 + i][1])
        n2_sp = []
        HOD = 0
    Square.update()
    s_k, s_i = skan()
    if s_i != 0 and len(AvailablePlayerTurns()) == 0:
        GameOver(3)


def AvailableCompTurns():
    turns_list = looking_k1([])
    if not (turns_list):
        turns_list = looking_k2([])
    return turns_list


def CheckCompTurn(tur, n_turns_list, turns_list):
    global Board
    global n2_sp
    global l_rez, k_rez, o_rez
    if not turns_list:
        turns_list = AvailableCompTurns()
    if turns_list:
        k_Board = copy.deepcopy(Board)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                CheckCompTurn(tur, (n_turns_list + ((poz1_x, poz1_y),)), t_turns_list)
            else:
                CheckPlayerTurn(tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not n2_sp:
                        n2_sp = (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez
                    else:
                        if t_rez == l_rez:
                            n2_sp = n2_sp + (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez < l_rez:
                            n2_sp = (n_turns_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez
                    o_rez = 0
                    k_rez = 0
            Board = copy.deepcopy(k_Board)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def AvailablePlayerTurns():
    turns_list = looking_i1()
    if not turns_list:
        turns_list = looking_i2([])
    return turns_list


def CheckPlayerTurn(tur, turns_list):
    global Board, k_rez, o_rez
    global poz1_x, poz1_y, poz2_x, poz2_y
    global ur
    if not turns_list:
        turns_list = AvailablePlayerTurns()
    if turns_list:
        k_Board = copy.deepcopy(Board)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                CheckPlayerTurn(tur, t_turns_list)
            else:
                if tur < ur:
                    CheckCompTurn(tur + 1, (), [])
                else:
                    s_k, s_i = skan()
                    o_rez += (s_k - s_i)
                    k_rez += 1

            Board = copy.deepcopy(k_Board)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def skan():
    global Board
    s_i = 0
    s_k = 0
    for x in Board:
        for y in x:
            if y == 1: s_i += 1
            if y == 2: s_i += 3
            if y == 3: s_k += 1
            if y == 4: s_k += 3

    if s_i == 0 and HOD == 0:
        GameOver(2)
    elif s_k == 0 and HOD == 0:
        GameOver(1)
    return s_k, s_i


def PlayerTurn():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global HOD
    HOD = 1
    turns_list = AvailablePlayerTurns()
    if turns_list:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in turns_list:
            t_turns_list = Turn(1, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_turns_list:
                HOD = 0
        else:
            HOD = 0
    Square.update()
    s_k, s_i = skan()
    if len(AvailableCompTurns()) == 0 and s_k != 0:
        GameOver(4)
    elif s_k == 0:
        GameOver(1)


def Turn(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global Board
    if f:
        draw_viv(poz1_x, poz1_y, poz2_x, poz2_y)
    if poz2_y == 0 and Board[poz1_y][poz1_x] == 1:
        Board[poz1_y][poz1_x] = 2
    if poz2_y == 11 and Board[poz1_y][poz1_x] == 3:
        Board[poz1_y][poz1_x] = 4
    Board[poz2_y][poz2_x] = Board[poz1_y][poz1_x]
    Board[poz1_y][poz1_x] = 0
    kx = ky = 1
    if poz1_x < poz2_x: kx = -1
    if poz1_y < poz2_y: ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if Board[y_poz][x_poz] != 0:
            Board[y_poz][x_poz] = 0
            if f:
                draw_viv(-1, -1, -1, -1)
            if Board[poz2_y][poz2_x] == 3 or Board[poz2_y][poz2_x] == 4:
                return looking_k1p([], poz2_x, poz2_y)
            elif Board[poz2_y][poz2_x] == 1 or Board[poz2_y][poz2_x] == 2:
                return looking_i1p([], poz2_x, poz2_y)
    if f:
        draw_viv(poz1_x, poz1_y, poz2_x, poz2_y)


def looking_k1(turns_list):
    for y in range(12):
        for x in range(12):
            turns_list = looking_k1p(turns_list, x, y)
    return turns_list


def looking_k1p(turns_list, x, y):
    if Board[y][x] == 3:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 11 and 0 <= x + ix + ix <= 11:
                if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    if Board[y][x] == 4:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 12):
                if 0 <= y + iy * i <= 11 and 0 <= x + ix * i <= 11:
                    if osh == 1:
                        turns_list.append(((x, y), (x + ix * i, y + iy * i)))
                    if Board[y + iy * i][x + ix * i] == 1 or Board[y + iy * i][x + ix * i] == 2:
                        osh += 1
                    if Board[y + iy * i][x + ix * i] == 3 or Board[y + iy * i][x + ix * i] == 4 or osh == 2:
                        if osh > 0: turns_list.pop()
                        break
    return turns_list


def looking_k2(turns_list):
    for y in range(12):
        for x in range(12):
            if Board[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 11 and 0 <= x + ix <= 11:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 1 or Board[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 11 and 0 <= x + ix * 2 <= 11:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if Board[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 12):
                        if 0 <= y + iy * i <= 11 and 0 <= x + ix * i <= 11:
                            if Board[y + iy * i][x + ix * i] == 0:
                                turns_list.append(((x, y), (x + ix * i, y + iy * i)))
                            if Board[y + iy * i][x + ix * i] == 1 or Board[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if Board[y + iy * i][x + ix * i] == 3 or Board[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return turns_list


def looking_i1():
    turns_list = []
    for y in range(12):
        for x in range(12):
            turns_list = looking_i1p(turns_list, x, y)
    return turns_list


def looking_i1p(turns_list, x, y):
    if Board[y][x] == 1:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 11 and 0 <= x + ix + ix <= 11:
                if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                    if Board[y + iy + iy][x + ix + ix] == 0:
                        turns_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    if Board[y][x] == 2:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 12):
                if 0 <= y + iy * i <= 11 and 0 <= x + ix * i <= 11:
                    if osh == 1:
                        turns_list.append(((x, y), (x + ix * i, y + iy * i)))
                    if Board[y + iy * i][x + ix * i] == 3 or Board[y + iy * i][x + ix * i] == 4:
                        osh += 1
                    if Board[y + iy * i][x + ix * i] == 1 or Board[y + iy * i][x + ix * i] == 2 or osh == 2:
                        if osh > 0: turns_list.pop()
                        break
    return turns_list


def looking_i2(turns_list):
    for y in range(12):
        for x in range(12):
            if Board[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 11 and 0 <= x + ix <= 11:
                        if Board[y + iy][x + ix] == 0:
                            turns_list.append(((x, y), (x + ix, y + iy)))
                        if Board[y + iy][x + ix] == 3 or Board[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 11 and 0 <= x + ix * 2 <= 11:
                                if Board[y + iy * 2][x + ix * 2] == 0:
                                    turns_list.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if Board[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 12):
                        if 0 <= y + iy * i <= 11 and 0 <= x + ix * i <= 11:
                            if Board[y + iy * i][x + ix * i] == 0:
                                turns_list.append(((x, y), (x + ix * i, y + iy * i)))
                            if Board[y + iy * i][x + ix * i] == 3 or Board[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if Board[y + iy * i][x + ix * i] == 1 or Board[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return turns_list


def run():
    start_game()
    draw_viv(-1, -1, -1, -1)
    Square.bind("<Motion>", HighlightCell)
    Square.bind("<Button-1>", ClickHandler)
    mainloop()


if __name__ == "__main__":
    run()