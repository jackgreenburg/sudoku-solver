from math import floor
import tkinter as tk

# same as version 3 except entering sudoku with tkinter
# COMPILER DEFINED THINGS !!
# numbers=[81,80,79,78,77,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
# numbers=[0,0,0,8,0,0,0,0,9,0,0,4,0,0,0,0,0,0,5,2,0,0,0,4,8,0,0,0,0,0,0,2,0,4,0,0,0,0,0,1,5,0,0,6,0,6,0,0,0,0,0,0,0,8,0,8,2,0,0,9,1,0,0,0,0,0,0,0,0,3,0,0,0,1,6,7,3,0,0,0,0]
sudoku1 = [0, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 9, 0, 3, 0, 0, 0, 0, 3, 0, 1, 0, 0, 9, 0, 4, 0, 8, 2, 0, 5, 0, 6,
           0, 0, 0, 0, 0, 6, 9, 0, 0, 6, 0, 0, 0, 5, 0, 0, 0, 3, 3, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0,
           0, 0, 8, 0, 0, 0, 0, 0, 0]
sudoku1 = [5, 3, 0, 0, 7, 0, 0, 0, 0, 6, 0, 0, 1, 9, 5, 0, 0, 0, 0, 9, 8, 0, 0, 0, 0, 6, 0, 8, 0, 0, 0, 6, 0, 0, 0, 3,
           4, 0, 0, 8, 0, 3, 0, 0, 1, 7, 0, 0, 0, 2, 0, 0, 0, 6, 0, 6, 0, 0, 0, 0, 2, 8, 0, 0, 0, 0, 4, 1, 9, 0, 0, 5,
           0, 0, 0, 0, 8, 0, 0, 7, 9]
total = sudoku1.count(0)

# numbers=[6,9,3,0,7,0,0,0,5,0,4,0,0,5,9,2,6,0,0,2,0,8,0,6,4,9,0,4,0,2,6,9,0,0,5,0,8,0,0,0,3,5,9,0,4,3,0,9,0,0,8,0,7,1,0,0,0,9,0,4,7,3,6,2,6,7,5,8,0,0,0,0,0,3,4,1,0,0,5,0,2]
# numbersS=[6,9,3,4,7,2,8,1,5,1,4,8,3,5,9,2,6,0,0,2,0,8,0,6,4,9,0,4,0,2,6,9,0,0,5,0,8,0,0,0,3,5,9,0,4,3,0,9,0,0,8,0,7,1,0,0,0,9,0,4,7,3,6,2,6,7,5,8,0,0,0,0,0,3,4,1,0,0,5,0,2]
boxIndex = [0, 1, 2, 9, 10, 11, 18, 19, 20, 3, 4, 5, 12, 13, 14, 21, 22, 23, 6, 7, 8, 15, 16, 17, 24, 25, 26, 27, 28,
            29, 26, 27, 28, 45, 46, 47, 30, 31, 32, 39, 40, 41, 48, 49, 50, 33, 34, 35, 42, 43, 44, 51, 52, 53, 54, 55,
            56, 63, 64, 65, 72, 73, 74, 57, 58, 59, 66, 67, 68, 75, 76, 77, 60, 61, 62, 69, 70, 71, 78, 79,
            80]  # [0,3,6,1,5,7,2,4,8]
columnIndex = [0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5, 6, 7, 8, 6, 7, 8, 6, 7, 8, 0, 1, 2, 0, 1, 2, 0, 1,
               2, 3, 4, 5, 3, 4, 5, 3, 4, 5, 6, 7, 8, 6, 7, 8, 6, 7, 8, 0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 4, 5, 3, 4, 5, 3,
               4, 5, 6, 7, 8, 6, 7, 8, 6, 7, 8]


# reminder: whenever you recompile, must re break
class Box:  # not used at the moment
    def __init__(self):
        self.possibles = [[True for _ in range(9)] for _ in range(9)]


class Puzzle:  # not used at the moment
    def __init__(self, p):
        self.puzzle = p

    def __init__(self):
        print("called")
        Window = tk.Tk()
        print("entered: ", 9, 9)
        for i in range(9):
            Window.columnconfigure(i, )  # weight=1, minsize=50)
            Window.rowconfigure(i, )  # weight=1, minsize=50)
            for j in range(0, 9):
                entry = tk.Entry(master=Window, width=3)  # {i} Column {j}")
                rightPad = 0
                bottomPad = 0
                if j == 2 or j == 5:
                    rightPad = 5
                if i == 2 or i == 5:
                    bottomPad = 5
                entry.grid(row=i, column=j, padx=(0, rightPad), pady=(0, bottomPad))
        entries = Window.grid_slaves(row=None, column=None)
        copyBtn = tk.Button(master=Window, text="Enter", width=10, command=lambda: solveSudoku(entries))
        copyBtn.grid(row=9, column=0, columnspan=9)

        # print(Window.grid_slaves(row=None, column=None))
        Window.mainloop()

    def __str__(self):
        for i in range(9):
            if i == 0 or i == 3 or i == 6:
                print("-------------------------------------")
            else:
                print("")
            line = ""
            for n in range(9):
                if n == 0 or n == 3 or n == 6:
                    line = line + "| " + str(self.puzzle[n + (i * 9)]) + " "
                else:
                    line = line + "  " + str(self.puzzle[n + (i * 9)]) + " "
            print(line + "|")
        print("-------------------------------------")


def display(numbers):
    for i in range(9):
        if i == 0 or i == 3 or i == 6:
            print("-------------------------------------")
        else:
            print("")
        line = ""
        for n in range(9):
            if n == 0 or n == 3 or n == 6:
                line = line + "| " + str(numbers[n + (i * 9)]) + " "
            else:
                line = line + "  " + str(numbers[n + (i * 9)]) + " "
        print(line + "|")
    print("-------------------------------------")


# take list and return columns
def breakColumns(code):
    columns = []

    for i in range(9):
        sColumn = []
        for n in range(81):
            if n % 9 == i:
                sColumn.append(code[n])
        columns.append(sColumn)
    return columns


# take list and return rows
def breakRows(code):
    return [code[9 * i:9 * i + 9] for i in range(9)]


# take list and return boxes
def breakBoxes(code):
    boxes = []
    for f in range(3):  # row of box in puzzle
        for i in range(3):  # column of box in puzzle
            sBox = []
            for n in range(3):  # row of cell in box
                c = 9 * n + i * 3 + f * 27
                sBox.append(code[c])
                sBox.append(code[c + 1])
                sBox.append(code[c + 2])
            boxes.append(sBox)
    return boxes


# take boxes and return list
def compileBoxes(boxes):
    numbers = []
    for i in range(81):
        numbers.append(0)
    for box in range(9):
        for cell in range(9):
            numberIndex = int((27 * floor(box / 3)) + (3 * (box % 3)) + (9 * floor(cell / 3)) + (cell % 3))
            numbers[numberIndex] = boxes[box][cell]
    return numbers


def compileRows(rows):
    numbers = []
    for i in range(9):
        numbers.extend(rows[i])
    return numbers


# Box focused break down:
# 1. For all boxes, for all digits, checks all cells in box if digit can go there
#  a. checks rows, columns, and box for conflicts
# 2. If a digit can only go in one cell in a box, the value gets filled in
def checkPuzzleAdvanced(code):
    rows = breakRows(code)
    columns = breakColumns(code)
    boxes = breakBoxes(code)

    for box in range(9):  # loop through boxes
        for digit in range(1, 10):  # loop through digits
            # checks if all cells of box are valid sports for digit
            values = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # "index" of box
            for checkNum in range(9):
                # print("---", floor(box/3), box%3)
                if boxes[box][checkNum] != 0 or digit in rows[
                    3 * floor(box / 3) + floor(checkNum / 3)] or digit in columns[
                    3 * (box % 3) + checkNum % 3]:
                    values[checkNum] = 1
            numZeros = values.count(0)
            # loop through cells in box
            for cell in range(9):
                if digit not in boxes[box]:
                    row = 3 * floor(box / 3) + floor(cell / 3)
                    numb = (27 * floor(box / 3)) + (3 * (box % 3)) + (9 * floor(cell / 3)) + (
                            cell % 3)  # this is the current cells index position, i think
                    column = numb % 3 + 3 * (floor(numb / 3) % 3)  # columnIndex[counter]


                    if numZeros == 1 and digit not in boxes[box] and digit not in rows[row] and digit not in \
                            columns[column] and rows[row][column] == 0:
                        print(f"Row: {row}  column: {column}  becomes: {digit}  in box: {box + 1}  cell {cell + 1}")
                        rows[row][column] = digit
                        numeros = compileRows(rows)
                        columns = breakColumns(numeros)
                        boxes = breakBoxes(numeros)
                    elif numZeros == 2:
                        print(f"Box: {box+1}, digit: {digit}, cell: {cell+1}, values: {values}")
            # check if zeros remaning equals 2 for 2 digits
            # compare to other

    numeros = compileRows(rows)
    return numeros


def getSudoku():
    print("called")
    Window = tk.Tk()

    for i in range(9):
        # print("i", i)
        Window.columnconfigure(i, )  # weight=1, minsize=50)
        Window.rowconfigure(i, )  # weight=1, minsize=50)
        for j in range(0, 9):
            entry = tk.Entry(master=Window, width=3, justify='center')  # {i} Column {j}")
            rightPad = 0
            bottomPad = 0
            if j == 2 or j == 5:
                rightPad = 5
            if i == 2 or i == 5:
                bottomPad = 5
            entry.grid(row=i, column=j, padx=(0, rightPad), pady=(0, bottomPad))

    # child.rowconfigure(rows, )
    entries = Window.grid_slaves(row=None, column=None)
    copyBtn = tk.Button(master=Window, text="Enter", width=10, command=lambda: solveSudoku(entries))
    copyBtn.grid(row=9, column=0, columnspan=9)

    # print(Window.grid_slaves(row=None, column=None))
    Window.mainloop()


def solveSudoku(p):  # , puzzle):
    if not isinstance(p[0], int):  # check if entries are passed
        numbers = [0 for i in range(81)]
        for i, entry in enumerate(p):
            if entry := entry.get():
                numbers[80 - i] = int(entry)
    else:
        numbers = p
    # print(numbers)
    display(numbers)

    print("Found using basic means of comparison:")
    checker = []
    while 0 in numbers:
        # for _ in range(1):
        checker = numbers
        numbers = checkPuzzleAdvanced(numbers)
        if checker == numbers:
            print("Too hard...for normal methods...")
            display(numbers)
            popup(numbers)
            return False
        elif 0 not in numbers:  # check if done
            display(numbers)
            print("Done.")
            popup(numbers)
            return True
        break  #####
    popup(numbers)


def popup(p):
    print("Popup opened.")
    child = tk.Tk()

    rows = breakRows(p)
    for i in range(9):
        child.columnconfigure(i, )  # weight=1, minsize=50)
        child.rowconfigure(i, )  # weight=1, minsize=50)
        for j in range(0, 9):
            rightPad = 0
            bottomPad = 0
            if j == 2 or j == 5:
                rightPad = 4
            if i == 2 or i == 5:
                bottomPad = 4
            label = tk.Label(master=child, width=2, text=rows[i][j], borderwidth=0, background="white")
            label.grid(row=i, column=j, padx=(1, rightPad), pady=(2, bottomPad))
    child.mainloop()


display(
    [0, 0, 0, 0, 0, 0, 0, 2, 8, 0, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 4, 0, 1, 0, 0, 0, 5, 0, 0, 9, 7, 0, 3, 0, 0, 2, 0,
     4, 0, 0, 8, 0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0, 0, 1, 3, 0, 0, 9, 0, 0, 0, 0, 0, 5, 7, 0, 0, 2, 0, 9, 0, 0, 0, 8, 3,
     1, 7, 0, 0, 0])

# getSudoku()

solveSudoku(sudoku1)
#Puzzle()
