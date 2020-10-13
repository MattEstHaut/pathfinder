PATH     = 0
WALL     = 1
START    = 2
END      = 3
BANNED   = 4
SOLUTION = 5

def convert(labyrinth, config):
    for c in range(len(labyrinth)):
        for r in range(len(labyrinth[c])):
            labyrinth[c][r] = config[labyrinth[c][r]]
    return labyrinth

def findStart(labyrinth):
    for c in range(len(labyrinth)):
        for r in range(len(labyrinth[c])):
            if labyrinth[c][r] == START:
                return (c, r)
    return False

def getCross(labyrinth, center):
    directions = []
    cases = []
    if center[0] > 0 and center[0] < len(labyrinth) and center[1] >= 0 and center[1] < len(labyrinth[center[0]-1]):
        directions.append((center[0]-1, center[1]))
        cases.append(labyrinth[center[0]-1][center[1]])
    if center[0] >= 0 and center[0] < len(labyrinth)-1 and center[1] >= 0 and center[1] < len(labyrinth[center[0]+1]):
        directions.append((center[0]+1, center[1]))
        cases.append(labyrinth[center[0]+1][center[1]])
    if center[0] >= 0 and center[0] < len(labyrinth) and center[1] > 0 and center[1] < len(labyrinth[center[0]]):
        directions.append((center[0], center[1]-1))
        cases.append(labyrinth[center[0]][center[1]-1])
    if center[0] >= 0 and center[0] < len(labyrinth) and center[1] >= 0 and center[1] < len(labyrinth[center[0]])-1:
        directions.append((center[0], center[1]+1))
        cases.append(labyrinth[center[0]][center[1]+1])
    return directions, cases

def appendPath(labyrinth, paths):
    new_paths = []
    for path in paths:
        directions, cases = getCross(labyrinth, path[-1])
        if END in cases:
            path.append(directions[cases.index(END)])
            return path, True
        
        for d in range(len(directions)):
            if cases[d] == PATH:
                new_paths.append(path.copy())
                new_paths[-1].append(directions[d])
                labyrinth[directions[d][0]][directions[d][1]] = BANNED

    return new_paths, False

def resolve(labyrinth):
    paths = [[findStart(labyrinth)]]
    end = False
    while not end:
        paths, end = appendPath(labyrinth, paths)
        if len(paths) == 0:
            return False
    return paths

def labyrinthToString(labyrinth):
    string = ""
    for column in labyrinth:
        if string != "":
            string += "\n"
        for case in column:
            if case == PATH:
                string += " "
            elif case == WALL:
                string += "#"
            elif case == START:
                string += "S"
            elif case == END:
                string += "E"
            elif case == SOLUTION:
                string += "."
            elif case == BANNED:
                string += " "
    return string

if __name__ == "__main__":
    import sys, time

    if len(sys.argv) > 1:
        file = open(sys.argv[1], "r").read()
        configuration = {file[2]: START, file[4]: END, file[6]: PATH, file[8]: WALL}
        labyrinth = file.split("\n")
        labyrinth = labyrinth[1::]
        for c in range(len(labyrinth)):
            labyrinth[c] = list(labyrinth[c])
        convert(labyrinth, configuration)

        t = time.time()
        solution = resolve(labyrinth)
        t = int((time.time() - t) * 10**6)

        if solution is not False:
            if "-show" in sys.argv:
                for step in range(1, len(solution)-1):
                    labyrinth[solution[step][0]][solution[step][1]] = SOLUTION
                print(labyrinthToString(labyrinth))
            else:
                print(solution)
            print("Steps : ", len(solution)-1, ".", sep="")
            if (t > 1000):
                print("Calculated in ", int(t/1000), " ms.", sep="")
            else:
                print("Calculated in ", t, " µs.", sep="")
        else:
            print("No solution.")
    elif sys.argv[0] == "pathfinder.py":
        print("Usage: pathfinder.py [file]")