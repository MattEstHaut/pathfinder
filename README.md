# Pathfinder
A simple path finding algorithm.

### Python documentation

The labyrinth must be a two-dimensional array with distinct values for: paths, walls, departure and arrival. It will have to be converted into a maze usable by **pathfinder.py** as follows :

```
configuration = {"path": pathValue, "wall": wallValue, "start": startValue, "end": endValue}
labyrinth = pathfinder.convert_labyrinth(labyrinth, configuration)
```

Once this is done, you can calculate the shortest route to the finish :

```
solution = pathfinder.resolve(labyrinth)
```

You will get an array containing an ordered list of the coordinates of the shortest path. If there is no solution, the array will be zero length.

You can also solve a labyrinth contained in a file, labyrinth.lbrth is an example of a labyrinth stored in a :

```
[SSEEP W#]
#S########
#      ###
# ## #  ##
# #  ## ##
#   #   ##
##### ####
##       E
## ## ####
##    ####
##########
```

The first line means: "The starting point is represented by 'S', the end point is represented by 'E', the paths are represented by ' ' and the walls by '#'". If for example you want to represent the start with a 'D', you must also change the 'S' (the second) of the first line to a 'D'. 
To resolve this labyrinth use the following command in a terminal :

```
python pathfinder.py [filename] -show
```



### Javascript documentation