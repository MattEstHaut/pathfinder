# Pathfinder
N-dimensional pathfinder optimized algoritm module.

- Supports temporal dimensions
- Determines the shortest path
- Supports multi-exit labyrinth

## Test yourself

You can access the demo [here](https://mattesthaut.github.io/pathfinder) !
> This application uses an old version of pathfinder.js

## Quick start

Learn how to use the library through a simple example: the resolution of a two-dimensional labyrinth.

### Python3

First import the library like this :

```python
	import pathfinder
```

The labyrinth must be represented as a two-dimensional array of int, where the type of each case is represented by a specific value :

- 0: path
- 1: wall
- 2: starting point (there can be only one starting point)
- 3: exit (there can be several exits)

Here is an example of a valid two-dimensional labyrinth :

```python
labyrinth = [
    [0, 0, 0, 1, 3],
    [2, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 0, 3]
]
```
> Note that the labyrinth has 2 exits.

Now we can solve it like this :

```python
path = pathfinder.resolve(labyrinth)

if path is None:
    print("No solution")
else:
    print("Solved")
```

Path is a list of tuple representing the coordinates of the points travelled from the starting point to the exit.

```python
print(path) # -> [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (4, 2), (4, 3), (4, 4)]
```

### Javascript

First import the library like this :

```html
	<script src="pathfinder.js"></script>
```
> Must be before the implementation of your code.

The labyrinth must be represented as a two-dimensional array of int, where the type of each case is represented by a specific value :

- 0: path
- 1: wall
- 2: starting point (there can be only one starting point)
- 3: exit (there can be several exits)

Here is an example of a valid two-dimensional labyrinth :

```javascript
var labyrinth = [
    [0, 0, 0, 1, 3],
    [2, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 0, 3]
];
```
> Note that the labyrinth has 2 exits.

Now we can solve it like this :

```javascript
var path = PATHFINDER.resolve(labyrinth);

if (!path) {
    console.log("No solution")
} else {
	console.log("Solved")
}

// here path = [[1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [4, 2], [4, 3], [4, 4]]
```

Path is a bidimensional array representing the coordinates of the points travelled from the starting point to the exit.