# Pathfinder
A simple path finding algorithm.

### Test yourself

You can access the application by clicking [here](https://mattesthaut.github.io/pathfinder) !

### Python documentation

First, import the package :

```python
import pathfinder.py
```

The labyrinth must be a two-dimensional array with distinct values for: paths, walls, departure and arrival. It will have to be converted into a labyrinth usable by **pathfinder.py** as follows :

```python
configuration = {"path": pathValue, "wall": wallValue, "start": startValue, "end": endValue}
labyrinth = pathfinder.convert_labyrinth(labyrinth, configuration)
```

Once this is done, you can calculate the shortest route to the finish :

```python
solution = pathfinder.resolve(labyrinth)
```

You will get an array containing an ordered list of the coordinates of the shortest path. If there is no solution, the array will be zero length.

You can also solve a labyrinth contained in a file, labyrinth.lbrth is an example of a labyrinth stored in a file :

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

```python
python pathfinder.py [filename] -show
```


### Javascript documentation

First, import the package :

```html
<script type="text/javascript" src="pathfinder.js"></script>
```

The labyrinth must be a two-dimensional array with distinct values for: paths, walls, departure and arrival. It will have to be converted into a labyrinth usable by **pathfinder.js** as follows :

```javascript
const configuration = {path: pathValue, wall: wallValue, start: startValue, end: endValue};
labyrinth = PATHFINDER.convert_labyrinth(labyrinth, configuration);
```

Once this is done, you can calculate the shortest route to the finish :

```javascript
var solution = PATHFINDER.resolve(labyrinth);
```

You will get an array containing an ordered list of the coordinates of the shortest path. If there is no solution, the array will be zero length.

You can export a labyrinth as a file:

```javascript
PATHFINDER.export(labyrinth);
```
> This file is readable for **pathfinder.py**

You can import a labyrinth like this:

```html
<input type="file" id="reader" />
```
```javascript
const reader = document.getElementById("reader");

PATHFINDER.import(reader, (labyrinth) => {
	//some code...
})
```
> **pathfinder.js** can read the same type of file as **pathfinder.py**.
