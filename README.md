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

### Javascript documentation