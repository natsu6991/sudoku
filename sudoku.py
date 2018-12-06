import sys
import time
import numpy as np
import imp
from random import randint, shuffle
# import files contains sudokus (easy, medium, hard) and the generated sudoku
import sudokus
import generated

# check if each line is completed
def validRow(e,x):
	for i in range(0,9):
		if grid[x][i] == e:
			return False
	return True

# check if each column is completed
def validCol(e,y):
	for i in range(0,9):
		if grid[i][y] == e:
			return False
	return True

# check if each box is completed
def validBox(e,x,y):
	row = x-x%3
	col = y-y%3
	for i in range(3):
		for z in range(3):
			if(grid[i+row][z+col] == e):
				return False
	return True

# check if each line, row and box (or the sudoko himself) is completed
def isValid(e,x,y):
	return validRow(e,x) and validCol(e,y) and validBox(e,x,y)

next_empty = [0,0]

# find all the empty slot
def empty():
	for x in range(0,9):
		for y in range(0,9):
			if grid[x][y] == 0:
				global next_empty
				next_empty = [x,y]
				return True
	return False

# get all empty slot and insert numbers in the empty slot
def solve():
	if not(empty()):
		return True
	x = next_empty[0]
	y = next_empty[1]

	for e in range(1,10):
		if(isValid(e,x,y)):
			grid[x][y] = e
			if solve():
				return True
			grid[x][y] = 0
	return False

# yes or no to use the solver
def solve_or_not():
	secondQuestion = input("\nDo you want to solve this sudoku (yes) or to leave (no) ?")
	if(secondQuestion == "yes" or secondQuestion == "y"):
		print("\n\nAlright, now we transfer the generated sudoku to the solver !!\n")
	elif(secondQuestion == "no" or secondQuestion == "n"):
		print("\nYou can get the generated sudoku in \"generated.py\" !")
		print("/!\ \n")
		exit()
	else:
		print("Please enter \"yes\" or \"no\" (or \"y\" or \"n\")")
		solve_or_not()

# yes or no to choose the sudoku generated
def yes_or_no(grid):
	firstQuestion = input("\nDo you want to continue with this sudoku (yes) or generate an another (no) ?")
	if(firstQuestion == "yes" or firstQuestion == "y"):
		# replace in generated.py the new random sudoku generated
		fileRandom = open("generated.py", "w")
		fileRandom.write("randomSudoku = [\n")
		indexLine = 0
		for line in grid:
			indexLine += 1
			fileRandom.write("	[")
			indexElem = 0
			for elem in line:
				indexElem += 1
				fileRandom.write(str(elem))
				if indexElem != 9:
					fileRandom.write(", ")
			fileRandom.write("]")
			if indexLine != 9:
				fileRandom.write(",")
			fileRandom.write("\n")
		fileRandom.write("]")
		fileRandom.close()
		return solve_or_not()
	elif(firstQuestion == "no" or firstQuestion == "n"):
		return random_sudoku()
	else:
		print("Please enter \"yes\" or \"no\" (or \"y\" or \"n\")")
		yes_or_no()

# generate a random sudoku
def random_sudoku():
	zero = np.zeros((9,9),dtype=int)
	flist = [1,2,3,4,5,6,7,8,9]
	shuffle(flist)
	for i in range(0,9):
		zero[i][0] = flist[i]
	global grid
	grid = zero
	solve()
	for i in range(0,9):
		for j in range(0,9):
			randomNot = randint(0,4)
			randomYes = randint(0,2)
			if randomNot != randomYes:
				zero[i][j] = 0
	sudoku(zero)
	yes_or_no(zero)

# construct sudoku view in shell
def sudoku(board):
	print("+" + "-------+"*3)
	for i, row in enumerate(board):
		print(("|" + " {} {} {} |"*3).format(*[x if x != 0 else " " for x in row]))
		if i % 3 == 2:
			print("+" + "-------+"*3)

# add a parameter (sudoku choice) to choose by the user
print('')
if len(sys.argv) > 1:
	path = sys.argv[1]
	if path == "easy":
		grid = sudokus.easy
	elif path == "medium":
		grid = sudokus.medium
	elif path == "hard":
		grid = sudokus.hard
	elif path == "random":
		random_sudoku()
		imp.reload(generated)
		grid = generated.randomSudoku
		print("")

	print('\x1b[1;35;40m' + "sudoku to resolve :" + '\x1b[0m')
	sudoku(grid)
	print('\x1b[1;35;40m' + "solve start" + '\x1b[0m')
	tmp1=time.time()
	solve()
	tmp2=time.time()-tmp1
	print("Execution time = %fs" %tmp2)
	print('\x1b[1;35;40m' + "solve finish" + '\x1b[0m')
	sudoku(grid)
else:
	print('\x1b[1;35;40m' + "Add one more parameter to select the sudoku to resolve with : " + '\x1b[0m' + "\"python3 sudoku.py easy\"")
	print('\x1b[1;35;40m' + "List of sudoku :" + '\x1b[0m')
	print('\x1b[1;32;40m' + "easy :" + '\x1b[0m')
	sudoku(sudokus.easy)
	print('\x1b[1;32;40m' + "medium :" + '\x1b[0m')
	sudoku(sudokus.medium)
	print('\x1b[1;32;40m' + "hard :" + '\x1b[0m')
	sudoku(sudokus.hard)
	print('\x1b[1;35;40m' + "Or using a random sudoku with " + '\x1b[0m' + "\"python3 sudoku.py random\"")
	print('Enjoy !!')
print('')
