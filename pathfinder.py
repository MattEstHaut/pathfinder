def convert_labyrinth(labyrinth, configuration):
	for column in range(len(labyrinth)):
		for row in range(len(labyrinth[column])):
			if labyrinth[column][row] == configuration["path"]:
				labyrinth[column][row] = 0
			elif labyrinth[column][row] == configuration["wall"]:
				labyrinth[column][row] = 1
			elif labyrinth[column][row] == configuration["start"]:
				labyrinth[column][row] = 2
			elif labyrinth[column][row] == configuration["end"]:
				labyrinth[column][row] = 3
	return labyrinth

def find_start(labyrinth):
	for column in range(len(labyrinth)):
		for row in range(len(labyrinth[column])):
			if labyrinth[column][row] == 2:
				return (column, row)
	return False

def get_cross(labyrinth, center):
	cross = [[1 for h in range(3)] for w in range(3)]
	if center[0] > 0 and center[0] < len(labyrinth) and center[1] >=  0 and center[1] < len(labyrinth[center[0]]):
		cross[0][1] = labyrinth[center[0]-1][center[1]]
	if center[0] >= 0 and center[0] < len(labyrinth)-1 and center[1] >=  0 and center[1] < len(labyrinth[center[0]]):
		cross[2][1] = labyrinth[center[0]+1][center[1]]
	if center[0] >= 0 and center[0] < len(labyrinth) and center[1] >  0 and center[1] < len(labyrinth[center[0]]):
		cross[1][0] = labyrinth[center[0]][center[1]-1]
	if center[0] >= 0 and center[0] < len(labyrinth) and center[1] >=  0 and center[1] < len(labyrinth[center[0]])-1:
		cross[1][2] = labyrinth[center[0]][center[1]+1]
	return cross

def get_possibilities(labyrinth, position):
	directions = []
	cases = []
	cross = get_cross(labyrinth, position)
	for column in range(3):
		for row in range(3):
			if  cross[column][row] in [0, 3]:
				directions.append((column-1+position[0], row-1+position[1]))
				cases.append(cross[column][row])
	return directions, cases

def labyrinth_to_string(labyrinth):
	string = ""
	for column in labyrinth:
		if string != "":
			string += "\n"
		for case in column:
			if case == 0:
				string += " "
			elif case == 1:
				string += "#"
			elif case == 2:
				string += "S"
			elif case == 3:
				string += "E"
			elif case == 4:
				string += "."
	return string

def calculate_paths(labyrinth, paths):
	new_paths = []
	for path in paths:
		directions, cases = get_possibilities(labyrinth, path[-1])
		if 3 in cases:
			new_paths = path.copy()
			new_paths.append(directions[cases.index(3)])
			return new_paths, True
		else:
			for direction in directions:
				if not (direction in path):
					new_paths.append(path.copy())
					new_paths[-1].append(direction)
	return new_paths, False

def resolve(labyrinth):
	paths = [[find_start(labyrinth)]]
	end = False
	while not end:
		paths, end = calculate_paths(labyrinth, paths)
		if len(paths) == 0:
			end = True
	return paths

def limit(labyrinth, width, height):
	new_labyrinth = []
	for column in range(width):
		new_labyrinth.append([])
		for row in range(height):
			new_labyrinth[column].append(labyrinth[column][row])
	return new_labyrinth

import sys
if len(sys.argv) > 1 and sys.argv[0] == "pathfinder.py":
	file = open(sys.argv[1], "r").read()
	configuration = {"start": file[2], "end": file[4], "path": file[6], "wall": file[8]}
	file = file[11:]
	width = file.index("\n")
	height = int((len(file)+1)/(width+1))
	labyrinth = file.split("\n")
	for column in range(len(labyrinth)):
		labyrinth[column] = list(labyrinth[column])
	convert_labyrinth(labyrinth, configuration)
	labyrinth = limit(labyrinth, width, height)
	solution = resolve(labyrinth)

	if len(solution) > 0:
		if "-show" in sys.argv:
			for step in range(1, len(solution)-1):
				labyrinth[solution[step][0]][solution[step][1]] = 4
			print(labyrinth_to_string(labyrinth))
		else:
			print(solution)
		print("Steps : ", len(solution)-1, ".", sep="")

	else:
		print("No solution.")
elif sys.argv[0] == "pathfinder.py":
	print("Usage: pathfinder.py [file]")