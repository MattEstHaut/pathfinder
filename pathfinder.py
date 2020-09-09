import sys
if len(sys.argv) > 1:
	file = open(sys.argv[1], "r").read()
	config = {"S": file[2], "E": file[4], "P": file[6], "W": file[8]}
	file = file[11:]
	width = file.index("\n")
	height = int((len(file)+1)/(width+1))
	labyrinth = file.split("\n")
	
	for row in range(height):
		if "S" in labyrinth[row]:
			start = (row, labyrinth[row].index(config["S"]))
			break

	def get_cross(center):
		cross = [[config["W"] for row in range(3)] for column in range(3)]
		if len(center) == 2:
			if center[0] > 0:
				cross[0][1] = labyrinth[center[0]-1][center[1]]
			if center[0] < height-1:
				cross[2][1] = labyrinth[center[0]+1][center[1]]
			if center[1] > 0:
				cross[1][0] = labyrinth[center[0]][center[1]-1]
			if center[1] < width-1:
				cross[1][2] = labyrinth[center[0]][center[1]+1]

		return cross

	paths = [["start", start]]
	blocked = False

	while not blocked:
		for path in paths:
			position = path[-1]
			cross = get_cross(position)
			possibilities = 0

			if cross[0][1] == config["P"] or cross[0][1] == config["E"]:
				direction = (position[0]-1, position[1])
				if not direction in path:
					path.append(direction)
					possibilities += 1

			if cross[2][1] == config["P"] or cross[2][1] == config["E"]:
				direction = (position[0]+1, position[1])
				if not direction in path:
					if possibilities > 0:
						paths.append(path.copy())
						paths[-1][-1] = direction
						possibilities += 1
					else:
						path.append(direction)
						possibilities += 1

			if cross[1][0] == config["P"] or cross[1][0] == config["E"]:
				direction = (position[0], position[1]-1)
				if not direction in path:
					if possibilities > 0:
						paths.append(path.copy())
						paths[-1][-1] = direction
						possibilities += 1
					else:
						path.append(direction)
						possibilities += 1

			if cross[1][2] == config["P"] or cross[1][2] == config["E"]:
				direction = (position[0], position[1]+1)
				if not direction in path:
					if possibilities > 0:
						paths.append(path.copy())
						paths[-1][-1] = direction
						possibilities += 1
					else:
						path.append(direction)
						possibilities += 1

			if possibilities == 0 and len(position) == 2:
				if len(position) == 2 and labyrinth[position[0]][position[1]] == config["E"]:
					path.append("end")
				else:
					path.append("blocked")

		blocked = True
		for path in paths:
			if len(path[-1]) == 2:
				blocked = False
				break

	solutions = []
	best_solution = False
	for path in paths:
		if path[-1] == "end":
			solutions.append(path)
			if not best_solution:
				best_solution = path
			elif len(best_solution) > len(path):
				best_solution = path

	if (len(solutions) > 0):
		best_solution_string = ""
		for step in best_solution:
			if len(step) == 2:
				best_solution_string += "("+str(step[0])+", "+str(step[1])+") => "
			elif step == "start":
				best_solution_string += "(start) => "
			elif step == "end":
				best_solution_string += "(end)"

		print("Solutions: ", len(solutions), ".", sep="")
		print("Best solution steps: ", len(best_solution)-3, ".", sep="")
		print("Best solution:", best_solution_string)
	else:
		print("No solution.")

else:
	print("Usage: pathfinder.py [file]")