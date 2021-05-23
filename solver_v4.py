"""
full sudoku generator, checker, and solver
upgrading from v2 to v3 makes slightly harder sudoku
fairly polished gui interactions
"""

import tkinter as tk
import random
import os.path
import numpy as np
import json


global regloops, boxloops, colloops, tranloops, found, trancalled
regloops, boxloops, colloops, tranloops, found, trancalled = 0, 0, 0, 0, 0, 0



# check a list of nine values to see what remains
# returns, perform and operation on returned set of values to get reduced set
def check9(nine):
    # False means empty, true means filled, loosely
    filledCells = [False for _ in range(9)]
    for i, cell in enumerate(nine):
        if cell.value != 0:
            filledCells[i] = True

    pencilMarksForNine = [[filledCells[i] for _ in range(9)] for i in range(9)]
    vals = {cell.value for cell in nine}
    for digit in range(1, 10):
        if digit in vals:  # if digit in box/col/row digit can't be in pencil marks
            for i in range(9):
                pencilMarksForNine[i][digit-1] = True
    for i, cellMarks in enumerate(pencilMarksForNine):
        nine[i].setPencilMarks(cellMarks)
    return pencilMarksForNine


def interpetPencil9(ninexnine):
    for cell in range(9):
        cellMarks = []
        for digit in range(9):
            if not ninexnine[digit][cell]:
                cellMarks.append(digit+1)
        print(cellMarks)


class Cell:
    def __init__(self, value, i):
        self.value = value
        self.pencilMarks = [False for _ in range(9)]
        self.rowIndex = i // 9
        self.colIndex = i % 9
        self.boxIndex = 3 * (i // 27) + (i % 9) // 3

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self) + str([i+1 for i in range(9) if not self.pencilMarks[i]])

    # be wary
    def __eq__(self, other):
        return self.value

    def setPencilMarks(self, pmarks):
        for i in range(9):
            self.pencilMarks[i] = self.pencilMarks[i] or pmarks[i]


class Puzzle:
    """
    initialization takes in list of values by rows
    """

    def __init__(self, puzzList):
        self.puzzList = puzzList
        self.cellsList = np.array([Cell(puzzList[i], i) for i in range(81)])
        self.puzzSolved = None
        # row then digit then column of box
        self.simplifiedRows = [[[False for _ in range(3)] for _ in range(9)] for _ in range(9)]
        # column then digit then row of box
        self.simplifiedCols = [[[False for _ in range(3)] for _ in range(9)] for _ in range(9)]

        #self.pencilMarks = [[] for _ in range(9)]

        # breakColumns(compileRows(column1PM))  # transpose by making into a single list, then getting columns
        # [[column1PM[j][i] for j in range(9)] for i in range(9)]  # transpose with list comprehension
        self.rowsMatrix = np.reshape(self.cellsList, (9, 9))  # get rows from 81x9 matrix (list of cells with 9 pencil marks per cell)
        self.colsMatrix = np.transpose(self.rowsMatrix)
        self.boxMatrix = breakBoxes(self.cellsList)


    def setBasicPencilMarks(self):
        for box in self.boxMatrix:
            check9(box)
        for row in self.rowsMatrix:
            check9(row)
        for col in self.colsMatrix:
            check9(col)

    """
    right now I'm thinking we need two types of pencil mark checking:
    1. check if any single digit is the only one that can be in a single cell
    2. check if any single cell is the only cell where any single digit can be
    all other methods will just be methods to update pencil marks
    """
    def checkPencilMarks(self):
        global regloops, boxloops, colloops, found
        # could be some symmetry here (if I was able to flip matrix) identifying column where there is one False
        # obviously, cols and rows are the same thing just flipped so you (me) are a moron
        # np array is faster sometimes but not all the time, I'm very confused
        # list comprehension is almost twice as fast as row compiling then breaking into columns
        for i, cell in enumerate(self.cellsList):
            ####
            #np.where(np.array(cell.pencilMarks) == False)
            ####
            if cell.pencilMarks.count(False) == 0 and cell.value == 0:
                print("FUCKFUCKFUCK")
            elif cell.pencilMarks.count(False) == 1:
                #print(f"row {i//9 + 1} col {i%9 + 1} becomes {cell.pencilMarks.index(False) + 1} due to it being the only valid digit for that cell")
                cell.value = cell.pencilMarks.index(False) + 1
                # can't do this because it might make another cell that doesn't have update pencil marks seem right
                #cell.setPencilMarks([True, True, True, True, True, True, True, True, True])
                #self.setBasicPencilMarks()
                found += 1
                self.updatePencilMarks(cell, cell.pencilMarks.index(False))
            regloops += 1

        # until I can selectively mark pencil marks upon changes
        # it is ~3 times faster to just risk calculating multiple values
        self.checkTranspose(self.boxMatrix, "boxes")
        self.checkTranspose(self.colsMatrix, "cols")
        self.checkTranspose(self.rowsMatrix, "rows")

    def checkTranspose(self, matrix, mtype):
        global trancalled
        trancalled += 1
        for i, subsect in enumerate(matrix):
            global tranloops, found
            # create a 9x9 matrix for the column containing the pencil marks
            colPencilMarks = np.array([cell.pencilMarks for cell in subsect])

            # transpose the pencil mark matrix to get it to be each row being a digit, the column being the cell
            for digit, pencilMarks in enumerate(np.transpose(colPencilMarks)):
                # this first check is unnecessary, its just security i guess
                tranloops += 1
                indices = np.where(pencilMarks == False)[0]
                if len(indices) == 1:
                    #print(f"row {subsect[indices[0]].rowIndex + 1 } col {subsect[indices[0]].colIndex + 1} becomes {digit + 1} due to it being the only valid cell for that digit (found in transpose func-{mtype})")

                    subsect[indices[0]].value = digit + 1
                    # must mark cell as filled
                    if True:  # update pencil marks on the fly
                        self.updatePencilMarks(subsect[indices[0]], digit)
                    found += 1


            # print(81 - compileRows(matrix).count("0")) #len(np.where(compileRows(matrix) == "0")[0]))

    def updatePencilMarks(self, cellToUpdate, digit):
        cellToUpdate.setPencilMarks([True, True, True, True, True, True, True, True, True])
        # must set all marks at that digit in column as filled
        for cell in self.colsMatrix[cellToUpdate.colIndex]:
            cell.pencilMarks[digit] = True
        # must set all marks at that digit in row as filled
        for cell in self.rowsMatrix[cellToUpdate.rowIndex]:
            cell.pencilMarks[digit] = True
        # must set all marks at that digit in box as filled
        for cell in self.boxMatrix[cellToUpdate.boxIndex]:
            cell.pencilMarks[digit] = True

    def checkSolved(self):
        for cell in self.cellsList:
            if cell.value == 0:
                return False
        return True

    """
    find square with two options, make new Puzzle and attempt to solve
    """
    def bowmansBingo(self):
        pass

    def setSimplified(self):
        # first loop over values to set simplified cols and rows arrays
        # this should not be done every time, one should be initialized and then updated (probably)
        # also, the values list is obviously done twice per cell per digit
        code = self.puzzList
        rows = breakRows(code)
        columns = breakColumns(code)
        boxes = breakBoxes(code)

        for box in range(9):  # loop through boxes
            for digit in range(1, 10):  # loop through digits
                # checks if all cells of box are valid sports for digit
                values = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # "index" of box
                if digit in boxes[box] or False:
                    for i in range(9):
                        values[i] = 1
                else:
                    for cell in range(9):
                        r = 3 * (box // 3) + (cell // 3)
                        c = 3 * (box % 3) + cell % 3
                        if boxes[box][cell] != 0 \
                                or digit in rows[r] \
                                or digit in columns[c] \
                                or self.simplifiedRows[r][digit - 1][box % 3] \
                                or self.simplifiedCols[c][digit - 1][box // 3]:
                            values[cell] = 1

                    # check if multiple of same are in a line
                    numZeros = values.count(0)
                    if numZeros == 2 or numZeros == 3:  # and digit not in boxes[box]:
                        cellOfZero = [i for i in range(9) if values[i] == 0]
                        doTheThingRows = True  # set to False to turn off rows matching
                        doTheThingCols = True  # set to False to turn off cols matching
                        for i in range(len(cellOfZero) - 1):
                            if not (cellOfZero[i] // 3) == (cellOfZero[i + 1] // 3):
                                doTheThingRows = False
                            if not cellOfZero[i] % 3 == cellOfZero[i + 1] % 3:
                                doTheThingCols = False
                        if doTheThingCols:
                            self.simplifiedCols[3 * (box % 3) + cellOfZero[0] % 3][digit - 1][(box // 3 + 1) % 3] = True
                            self.simplifiedCols[3 * (box % 3) + cellOfZero[0] % 3][digit - 1][(box // 3 + 2) % 3] = True
                        if doTheThingRows:
                            self.simplifiedRows[3 * (box // 3) + (cellOfZero[0] // 3)][digit - 1][(box + 1) % 3] = True
                            self.simplifiedRows[3 * (box // 3) + (cellOfZero[0] // 3)][digit - 1][(box + 2) % 3] = True

    # this code solves puzzles using only logical processes
    # it is needed in order to ensure puzzles can be solved without guessing
    # cannot easily use puzzle object that was used in v1 due to the recursion required
    def checkPuzzleAdvanced(self):
        code = self.puzzList
        rows = breakRows(code)
        columns = breakColumns(code)
        boxes = breakBoxes(code)
        # now loop over to check
        for box in range(9):  # loop through boxes
            for digit in range(1, 10):  # loop through digits
                # checks if all cells of box are valid sports for digit
                values = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # "index" of box
                if digit in boxes[box] or False:
                    for i in range(9):
                        values[i] = 1
                else:
                    for cell in range(9):
                        r = 3 * (box // 3) + (cell // 3)
                        c = 3 * (box % 3) + cell % 3
                        if boxes[box][cell] != 0 \
                                or digit in rows[r] \
                                or digit in columns[c] \
                                or self.simplifiedRows[r][digit - 1][box % 3] \
                                or self.simplifiedCols[c][digit - 1][box // 3]:
                            values[cell] = 1
                    numZeros = values.count(0)
                    # loop through cells in box
                    for cell in range(9):
                        if digit not in boxes[box]:
                            row = 3 * (box // 3) + (cell // 3)
                            numb = (27 * (box // 3)) + (3 * (box % 3)) + (9 * (cell // 3)) + (
                                    cell % 3)  # this is the current cells index position, i think
                            column = numb % 3 + 3 * ((numb // 3) % 3)  # columnIndex[counter]

                            if numZeros == 1 and digit not in rows[row] and digit not in \
                                    columns[column] and rows[row][column] == 0 and values[cell] == 0:
                                rows[row][column] = digit
                                numeros = compileRows(rows)
                                columns = breakColumns(numeros)
                                boxes = breakBoxes(numeros)
        return compileRows(rows)


# create new solved sudoku
def generate():
    row1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(row1)
    sudoku = [0 for _ in range(81)]
    for i, v in enumerate(row1):
        sudoku[i] = v
    return solve(sudoku)


# this code solves puzzles using only logical processes
# it is needed in order to ensure puzzles can be solved without guessing
# cannot easily use puzzle object that was used in v1 due to the recursion required
def checkPuzzleAdvanced(code):
    code = code
    rows = breakRows(code)
    columns = breakColumns(code)
    boxes = breakBoxes(code)

    # row then digit then column of box
    simplifiedRows = [[[False for _ in range(3)] for _ in range(9)] for _ in range(9)]  # True if value in sudoku
    # column then digit then row of box
    simplifiedCols = [[[False for _ in range(3)] for _ in range(9)] for _ in range(9)]

    # first loop over values to set simplified cols and rows arrays
    # this should not be done every time, one should be initialized and then updated (probably)
    # also, the values list is obviously done twice per cell per digit
    for box in range(9):  # loop through boxes
        for digit in range(1, 10):  # loop through digits
            # checks if all cells of box are valid sports for digit
            values = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # "index" of box
            if digit in boxes[box] or False:
                for i in range(9):
                    values[i] = 1
            else:
                for cell in range(9):
                    r = 3 * (box // 3) + (cell // 3)
                    c = 3 * (box % 3) + cell % 3
                    if boxes[box][cell] != 0 \
                            or digit in rows[r] \
                            or digit in columns[c] \
                            or simplifiedRows[r][digit-1][box % 3] \
                            or simplifiedCols[c][digit-1][box // 3]:
                        values[cell] = 1

                # check if multiple of same are in a line
                numZeros = values.count(0)
                if numZeros == 2 or numZeros == 3:  # and digit not in boxes[box]:
                    cellOfZero = [i for i in range(9) if values[i] == 0]
                    doTheThingRows = True  # set to False to turn off rows matching
                    doTheThingCols = True  # set to False to turn off cols matching
                    for i in range(len(cellOfZero)-1):
                        if not (cellOfZero[i]//3) == (cellOfZero[i+1]//3):
                            doTheThingRows = False
                        if not cellOfZero[i] % 3 == cellOfZero[i+1] % 3:
                            doTheThingCols = False
                    if doTheThingCols:
                        simplifiedCols[3*(box % 3) + cellOfZero[0] % 3][digit - 1][(box//3 + 1) % 3] = True
                        simplifiedCols[3*(box % 3) + cellOfZero[0] % 3][digit - 1][(box//3 + 2) % 3] = True
                    if doTheThingRows:
                        simplifiedRows[3*(box//3) + (cellOfZero[0]//3)][digit - 1][(box+1) % 3] = True
                        simplifiedRows[3*(box//3) + (cellOfZero[0]//3)][digit - 1][(box+2) % 3] = True

    # now loop over to check
    for box in range(9):  # loop through boxes
        for digit in range(1, 10):  # loop through digits
            # checks if all cells of box are valid sports for digit
            values = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # "index" of box
            if digit in boxes[box] or False:
                for i in range(9):
                    values[i] = 1
            else:
                for cell in range(9):
                    r = 3 * (box // 3) + (cell // 3)
                    c = 3 * (box % 3) + cell % 3
                    if boxes[box][cell] != 0 \
                            or digit in rows[r] \
                            or digit in columns[c] \
                            or simplifiedRows[r][digit-1][box % 3] \
                            or simplifiedCols[c][digit-1][box // 3]:
                        values[cell] = 1
                numZeros = values.count(0)
                # loop through cells in box
                for cell in range(9):
                    if digit not in boxes[box]:
                        row = 3 * (box // 3) + (cell // 3)
                        numb = (27 * (box // 3)) + (3 * (box % 3)) + (9 * (cell // 3)) + (
                                cell % 3)  # this is the current cells index position, i think
                        column = numb % 3 + 3 * ((numb // 3) % 3)  # columnIndex[counter]

                        if numZeros == 1 and digit not in rows[row] and digit not in \
                                columns[column] and rows[row][column] == 0 and values[cell] == 0:
                            rows[row][column] = digit
                            numeros = compileRows(rows)
                            columns = breakColumns(numeros)
                            boxes = breakBoxes(numeros)
    return compileRows(rows)


# check that puzzle can be solved without guessing
def checkValid(puzzle):
    while 0 in puzzle:
        checker = puzzle
        puzzle = checkPuzzleAdvanced(puzzle.copy())  # copy
        if checker == puzzle:
            return False
    return True  # check(puzzle)


# trim solution to create new puzzle
# if not set to end early trims, on average usually 25.24, has trimmed to as low as 23
def trim(solution):
    trimmed = solution.copy()
    indices = [i for i in range(81)]
    random.shuffle(indices)
    counter = 0  # number of filled squares
    for index in indices:
        trimmed[index] = 0
        if not checkValid(trimmed):
            trimmed[index] = solution[index]
        else:
            counter += 1
        if counter == 50 and False:  # change this for different difficulty
            break
    return trimmed


# solves sudoku recursively, inefficient
def solve(puzzle):
    if 0 not in puzzle:  # base case
        return puzzle

    for i, value in enumerate(puzzle):
        if value == 0:
            vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(vals)
            for d in vals:
                newPuzzle = puzzle
                newPuzzle[i] = d

                if checkCompatibility(newPuzzle, i):
                    newPuzzle = solve(newPuzzle)  # advance in recursion
                else:
                    newPuzzle[i] = 0
                if 0 not in newPuzzle:  # then it is solved, but I don't understand why this gets hit
                    return newPuzzle
                else:
                    pass  # continue guessing this cell
            puzzle[i] = 0
            return puzzle
    return puzzle


# checks tha a single new filled cell is legal
def checkCompatibility(puzzle, index):
    new = puzzle[index]
    row = (index // 9) * 9
    column = index % 9
    box = column // 3 + 3 * (row // 27)
    for i in range(9):
        if row + i != index:
            if puzzle[row + i] == new:
                return False
        if column+9*i != index:
            if puzzle[column + 9*i] == new:
                return False
        if (27 * (box // 3)) + (3 * (box % 3)) + (9 * (i // 3)) + (i % 3) != index:
            if puzzle[(27 * (box // 3)) + (3 * (box % 3)) + (9 * (i // 3)) + (i % 3)] == new:
                return False
    return True


# take list and return columns
def breakColumns(code):
    columns = [[None for _ in range(9)] for _ in range(9)]
    for i in range(81):
        columns[i % 9][i // 9] = code[i]
    return columns


# take list and return rows
def breakRows(code):
    return [code[9 * i:9 * i + 9] for i in range(9)]


# take list and return boxes
def breakBoxes(code):
    broken = np.zeros((9, 9), Cell)
    for i in range(81):
        broken[i // 9][i % 9] = code[int(i + 6 * ((i // 3) % 3 - (i % 27) // 9))]
    return broken

# take boxes and return list
def compileBoxes(boxes):
    numbers = [0 for _ in range(81)]
    for box in range(9):
        for cell in range(9):
            numberIndex = int((27 * (box // 3)) + (3 * (box % 3)) + (9 * (cell // 3)) + (cell % 3))
            numbers[numberIndex] = boxes[box][cell]
    return numbers


# take rows and return list
def compileRows(rows):
    numbers = []
    for i in range(9):
        numbers.extend(rows[i])
    return numbers


# open window displaying puzzle
def popup(p):
    child = tk.Tk()
    child.configure(background="black")
    rows = breakRows(p)
    for i in range(9):
        child.columnconfigure(i, )  # weight=1, minsize=50)
        child.rowconfigure(i, )  # weight=1, minsize=50)
        for j in range(0, 9):
            rightPad = 1
            bottomPad = 1
            if j == 2 or j == 5:
                rightPad = 3
            if i == 2 or i == 5:
                bottomPad = 3
            label = tk.Label(master=child, width=2, height=1, text=rows[i][j], borderwidth=0, background="gray95")
            label.grid(row=i, column=j, padx=(1, rightPad), pady=(1, bottomPad))
    child.mainloop()


# open solver window
def popupSolver(p):
    solution = solve(p.copy())
    child = tk.Tk()
    child.title("solver-v3")
    child.configure(background="black")
    rows = breakRows(p)
    for i in range(9):
        child.columnconfigure(i, )  # weight=1, minsize=50)
        child.rowconfigure(i, )  # weight=1, minsize=50)
        for j in range(0, 9):
            rightPad = 1
            bottomPad = 1
            if j == 2 or j == 5:
                rightPad = 3
            if i == 2 or i == 5:
                bottomPad = 3
            if rows[i][j] != 0:
                entry = tk.Entry(master=child, width=2, justify="center", borderwidth=0, background="gray70", )
                entry.insert(0, rows[i][j])
                entry.configure(state="disabled", disabledforeground="black", font=("Arial", 15))
            else:
                entry = tk.Entry(master=child, width=2, justify="center", borderwidth=0, bg="white", font=("Arial", 15))
            entry.grid(row=i, column=j, padx=(1, rightPad), pady=(1, bottomPad))
    entries = child.grid_slaves(row=None, column=None)

    solveBtn = tk.Button(master=child, text="Show Solution", width=12,  command=lambda: popup(solution))
    solveBtn.grid(row=9, column=4, columnspan=5)
    checkBtn = tk.Button(master=child, text="Check", width=12, command=lambda: checkSolution(getPuzz(entries), solution))
    checkBtn.grid(row=9, column=0, columnspan=5)
    child.update()
    child.mainloop()


# convert entry fields to a list
def getPuzz(entries):
    puzzle = [0 for _ in range(81)]
    for i in range(81):
        if (entry := entries[i].get()) != '':
            puzzle[80-i] = int(entry)
    return puzzle


# compare a puzzle to its solution
# open popup window with status
def checkSolution(puzzle, solution):
    correct = True
    done = True
    wrongCells = []
    for i in range(81):
        if puzzle[i] == 0:
            done = False
        elif puzzle[i] != solution[i]:
            correct = False
            wrongCells.append(f"[{i // 9 + 1}, {i % 9 + 1}]")
    if correct:
        if done:
            lblText = "Sudoku is solved!"
        else:
            lblText = "Sudoku is accurate so far!"
    else:
        innacuracies = "\n".join(wrongCells)
        lblText = f"Sudoku is innacurate at:\n{innacuracies}"
    # popup message
    status = tk.Tk()
    status.title("")  # set title of popup window
    lbl = tk.Label(status, text=lblText)
    lbl.pack(padx=12, pady=4)
    status.mainloop()


# main method basically
def home():
    root = tk.Tk()
    root.title("sudoku-v3")
    header = "Sudoku Solver V3"
    headLbl = tk.Label(master=root, text=header, font=("Arial", 25))
    headLbl.pack(padx=5)
    main = "Click the button to create a new\nrandomized sudoku."
    mainLbl = tk.Label(master=root, text=main, font=("Arial", 10))
    mainLbl.pack(padx=30)
    newBtn = tk.Button(master=root, text="Generate", font=("Arial", 15), width=12, command=lambda: popupSolver(trim(generate())))
    newBtn.pack(pady=(15, 10))
    # check if the logo exists in current directory
    if os.path.isfile("SudokuLogo.png"):
        icon1 = tk.PhotoImage(file="SudokuLogo.png")
        root.iconphoto(True, icon1)

    root.mainloop()


if __name__ == "__main__":
    #home()

    # parse x:
    with open('sudokus.json') as f:
        sudokus = json.load(f)

    easy1 = Puzzle(sudokus["easy1"])


    #popupSolver(sudokus["hard1"])

    import time
    response = "y"

    #print(np.where([False, True, False, True, True, False, False, False, False]))
    reps = 100
    start = time.time()
    for i in range(reps):
        hard1 = Puzzle(sudokus["hard1"])
        while (response == "y" or response[0] == "p") and True:
            hard1.setBasicPencilMarks()
            hard1.checkPencilMarks()
            #response = input("y/[n]:")
            if response[0] == "p":

                print(hard1.colsMatrix[0])
                print(hard1.rowsMatrix[0])
                hard1.colsMatrix[0][0] = False
                print(hard1.rowsMatrix[0])
                #print(hard1.boxMatrix[4])
                #print(hard1.colsMatrix[4])
                #print(hard1.rowsMatrix[4])
                #bxs = breakBoxes(hard1.cellsList)
                popup(hard1.cellsList)
            if hard1.checkSolved():
                #print("solved!")
                break
    end = time.time()
    print(end - start)
    print(regloops, boxloops, colloops, tranloops, found/reps, trancalled)
    popup(hard1.cellsList)
    print("correct ==", sudokus["hard1Solved"] == [cell.value for cell in hard1.cellsList])
    print(sudokus["hard1"].count(0))


