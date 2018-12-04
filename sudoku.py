import sys

easy = [
	[0, 0, 6, 0, 0, 0, 5, 0, 8],
	[1, 0, 2, 3, 8, 0, 0, 0, 4],
	[0, 0, 0, 2, 0, 0, 1, 9, 0],
	[0, 0, 0, 0, 6, 3, 0, 4, 5],
	[0, 6, 3, 4, 0, 5, 8, 7, 0],
	[5, 4, 0, 9, 2, 0, 0, 0, 0],
	[0, 8, 7, 0, 0, 4, 0, 0, 0],
	[2, 0, 0, 0, 9, 8, 4, 0, 7],
	[4, 0, 9, 0, 0, 0, 3, 0, 0],
]
medium = [
	[5, 3, 0, 0, 7, 0, 0, 0, 0],
	[6, 0, 0, 1, 9, 5, 0, 0, 0],
	[0, 9, 8, 0, 0, 0, 0, 6, 0],
	[8, 0, 0, 0, 6, 0, 0, 0, 3],
	[4, 0, 0, 8, 0, 3, 0, 0, 1],
	[7, 0, 0, 0, 2, 0, 0, 0, 6],
	[0, 6, 0, 0, 0, 0, 2, 8, 0],
	[0, 0, 0, 4, 1, 9, 0, 0, 5],
	[0, 0, 0, 0, 8, 0, 0, 7, 9],
]
hard = [
	[8, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 3, 6, 0, 0, 0, 0, 0],
	[0, 7, 0, 0, 9, 0, 2, 0, 0],
	[0, 5, 0, 0, 0, 7, 0, 0, 0],
	[0, 0, 0, 0, 4, 5, 7, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 3, 0],
	[0, 0, 1, 0, 0, 0, 0, 6, 8],
	[0, 0, 8, 5, 0, 0, 0, 1, 0],
	[0, 9, 0, 0, 0, 0, 4, 0, 0],
]

next_empty = [0,0]

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

# construct sudoku view in shell
def sudoku(board):
	print("+" + "-------+"*3)
	for i, row in enumerate(board):
		print(("|" + " {} {} {} |"*3).format(*[x if x != 0 else " " for x in row]))
		if i % 3 == 2:
			print("+" + "-------+"*3)

# add a parameter (sudoku choice) to choose by the user
if len(sys.argv) > 1:
	path = sys.argv[1]
	if path == "easy":
		grid = easy
	elif path == "medium":
		grid = medium
	elif path == "hard":
		grid = hard

	print('\x1b[1;35;40m' + "sudoku to resolve :" + '\x1b[0m')
	sudoku(grid)
	print('\x1b[1;35;40m' + "solve start" + '\x1b[0m')
	solve()
	print('\x1b[1;35;40m' + "solve finish" + '\x1b[0m')
	sudoku(grid)
else:
	print('\x1b[1;35;40m' + "Add one more parameter to select the sudoku to resolve like : " + '\x1b[0m' + "\"python3 sudoku.py easy\"")
	print('\x1b[1;32;40m' + "easy :" + '\x1b[0m')
	sudoku(easy)
	print('\x1b[1;32;40m' + "medium :" + '\x1b[0m')
	sudoku(medium)
	print('\x1b[1;32;40m' + "hard :" + '\x1b[0m')
	sudoku(hard)
