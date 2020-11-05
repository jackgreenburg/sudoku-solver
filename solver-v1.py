import math
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

class Puzzle:
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
        copyBtn = tk.Button(master=Window, text="Enter", width=10, command=lambda: solveSudoku(entries, self))
        copyBtn.grid(row=9, column=0, columnspan=9)

        print(Window.grid_slaves(row=None, column=None))
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
    rows = []
    for i in range(9):
        rows.append(code[i * 9:i * 9 + 9])
    return rows


# take list and return boxes
def breakBoxes(code):
    boxes = []
    for f in range(3):
        for i in range(3):
            sBox = []
            for n in range(3):
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
            numberIndex = int((27 * math.floor(box / 3)) + (3 * (box % 3)) + (9 * math.floor(cell / 3)) + (cell % 3))
            numbers[numberIndex] = boxes[box][cell]
    return numbers


def compileRows(rows):
    numbers = []
    for i in range(9):
        numbers.extend(rows[i])
    return numbers


# def compileColumns(columns):

"""
checkNumValues = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # if its the only one in the box with that number as an option...
for box in range(1):
    checkNumValues.append(box)
    print(checkNumValues)
    for cell in range(9):
        checkNumValues[cell] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for checkNum in range(9):
            checkNumValues[cell][checkNum] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
"""


def checkPuzzleAdvanced(code):
    rows = breakRows(code)
    columns = breakColumns(code)
    boxes = breakBoxes(code)
    for box in range(9):  # loop through boxes
        for digit in range(1, 10):  # loop through digits
            for cell in range(9):  # loop through cells in box ()
                if digit not in boxes[box]:
                    row = 3 * math.floor(box / 3) + math.floor(cell / 3)
                    numb = (27 * math.floor(box / 3)) + (3 * (box % 3)) + (9 * math.floor(cell / 3)) + (
                            cell % 3)  # this is the current cells index position, i think
                    column = numb % 3 + 3 * (math.floor(numb / 3) % 3)  # columnIndex[counter]
                    values = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                    for checkNum in range(9):  # checks box and surroundings of box for digit
                        if boxes[box][checkNum] != 0 or digit in rows[
                            3 * math.floor(row / 3) + math.floor(checkNum / 3)] or digit in columns[
                            3 * math.floor(column / 3) + checkNum % 3]:
                            values[checkNum] = 1
                    if values.count(0) == 1 and digit not in boxes[box] and digit not in rows[row] and digit not in \
                            columns[column] and rows[row][column] == 0:
                        n = 0
                        while values[n] != 0:
                            n += 1
                        print(f"Row: {row}  column: {column}  becomes: {digit}  in box: {box + 1}  cell {cell + 1}")
                        rows[row][column] = digit
                        numeros = compileRows(rows)
                        columns = breakColumns(numeros)
                        boxes = breakBoxes(numeros)

    numeros = compileRows(rows)
    return numeros


def getSudoku():
    print("called")
    Window = tk.Tk()

    # top=tk.Toplevel()
    # rows = 9
    # cols = 9

    print("entered: ", 9, 9)
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

    print(Window.grid_slaves(row=None, column=None))
    Window.mainloop()


def solveSudoku(entries): #, puzzle):
    numbers = [0 for i in range(81)]
    for i, entry in enumerate(entries):
        if entry := entry.get():
            numbers[80 - i] = int(entry)
    print(numbers)
    display(numbers)

    #checkPuzzleAdvanced
    checker = []
    while 0 in numbers:
        # for i in range (1):
        checker = numbers
        numbers = checkPuzzleAdvanced(numbers)
        if checker == numbers:
            print("Too hard...")
            display(numbers)
            break
        elif 0 not in numbers:
            display(numbers)
            print("Done.")
    popup(numbers)

def popup(p):
    print("oooo")
    #solveSudoku(p)
    child = tk.Tk()

    # top=tk.Toplevel()
    #rows = 9
    #cols = 9
    #list = []
    rows = breakRows(p)
    print(rows)
    print("entered: ", rows, 9)
    for i in range(9):
        # print("i", i)
        child.columnconfigure(i, )  # weight=1, minsize=50)
        child.rowconfigure(i, )  # weight=1, minsize=50)

        for j in range(0, 9):
            # print("j", j)
            # child.grid(row=i, column=j)

            label = tk.Label(master=child, width=3, text=rows[i][j])  # {i} Column {j}")
            # matrix[i, j] = entry
            label.grid(row=i, column=j)  # pack(padx=2, pady=2)

    # child.rowconfigure(rows, )
    #print(list)
    # for index, object in enumerate(child.grid_slaves(row=None, column=None)):
    #    print(object, index)
    #    matrix[i][j] = []
    #copyBtn = tk.Button(master=child, text="Copy", width=10, command=lambda: print("copy"))
    #copyBtn.grid(row=rows, column=0, columnspan=cols)

    print(child.grid_slaves(row=None, column=None))
    child.mainloop()


display(
    [0, 0, 0, 0, 0, 0, 0, 2, 8, 0, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 4, 0, 1, 0, 0, 0, 5, 0, 0, 9, 7, 0, 3, 0, 0, 2, 0,
     4, 0, 0, 8, 0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0, 0, 1, 3, 0, 0, 9, 0, 0, 0, 0, 0, 5, 7, 0, 0, 2, 0, 9, 0, 0, 0, 8, 3,
     1, 7, 0, 0, 0])
getSudoku()
