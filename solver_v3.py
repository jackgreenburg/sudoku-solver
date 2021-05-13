"""
full sudoku generator, checker, and solver
upgrading from v2 to v3 makes slightly harder sudoku
fairly polished gui interactions
"""

import tkinter as tk
import random
import os.path


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
    columns = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(81):
        columns[i % 9][i // 9] = code[i]
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
    home()
