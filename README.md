# Pathfinder
N-dimensional pathfinder optimized algoritm module.

- Supports temporal dimensions
- Determines the shortest path
- Supports multi-exit labyrinth

## Test yourself

You can access the demo [here](https://mattesthaut.github.io/pathfinder) !
> This application uses an old version of pathfinder.js

## Quick start

Learn how to use the library through a simple example : the resolution of a two-dimensional labyrinth.

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

## Solve more complex labyrinths

> ⚠️: first read [quick start](#Quick-start) !

We will see the more advanced features of the library through a new example: the resolution of a two-dimensional labyrinth that changes over time.

### Python3

Solving a two-dimensional labyrinth that changes over time is like solving a three-dimensional labyrinth (2 spatial dimensions and 1 temporal dimension) :

```python
t0 = [
    [0, 0, 0, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]

t1 = [
    [0, 0, 1, 0, 0],
    [2, 0, 0, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]

t2 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]

t3 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0]
]

t4 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

labyrinth = [t0, t1, t2, t3, t4] # labyrinth[t][x][y]
```

We have our three-dimensional labyrinth but we can't do :

```python
import pathfinder
path = pathfinder.resolve(labyrinth) # -> returns a wrong solution
```

The problem is that we have not specified that dimension 1 is a time dimension. A temporal dimension cannot be traversed in the same way as a spatial dimension : in a temporal dimension we can only move into the future and always by the same unit; that is, we must always increment the coordinates of the temporal dimension by a fixed value (in most cases by 1). 
The library has a panel of laws that define how to browse a dimension :

- pathfinder.FREE (default rule: the coordinate of a FREE dimension can be either incremented or decremented or remain fixed.)
- pathfinder.BLOCKED (the coordinate of a BLOCKED dimension always remains fixed.)
- pathfinder.FORWARD (the coordinate of a FORWARD dimension can be either incremented or remain fixed.)
- pathfinder.JUMP_FORWARD (the coordinate of a JUMP_FORWARD dimension is always incremented.)
- pathfinder.BACKWARD (the coordinate of a BACKWARD dimension can be either decremented or remain fixed.)
- pathfinder.JUMP_BACKWARD (the coordinate of a JUMP_BACKWARD dimension is always incremented.)

The JUMP_FORWARD law is perfectly adapted to run through a temporal dimension. let's specify that dimension 1 must follow this law :

```python
laws = pathfinder.newLaw(1, pathfinder.JUMP_FORWARD) # here, the dimension index starts at 1 and not at 0 

# We can add a law like this for example:
# laws = pathfinder.newLaw(2, pathfinder.FORWARD, laws)
```

We can try to solve the labyrinth :

```python
path = pathfinder.resolve(labyrinth, laws) # will return None
```

No path will be found yet we see that the labyrinth is resolvable, why ? It is simply that we arrive at the last coordinate of the first dimension (the time dimension) before having found the exit.
We can solve this problem like this :

```python
labyrinth = [t0, t1, t2, t3, t4, t0, t1, t2, t3, t4] # We repeat the transformation sequence once

laws = pathfinder.newLaw(1, pathfinder.JUMP_FORWARD)

path = pathfinder.resolve(labyrinth, laws) # returns -> [(0, 1, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 1), (5, 1, 1), (6, 1, 2), (7, 1, 3), (8, 1, 4)]
```
> Notice that each step of the path is represented by 3 coordinates because we have a three-dimensional labyrinth, the first coordinate is that of time.

It solves our problem, but it's not a clean way. How many times must the sequence be repeated for a more complex maze ? We can't know until we solve it. But we can add the sequence as we solve the labyrinthe thanks to the callback parameter :

```python
labyrinth = [t0, t1, t2, t3, t4]
laws = pathfinder.newLaw(1, pathfinder.JUMP_FORWARD)

t = 0 # represents time

def ourCallback(args): # our callback function
    global t
    global labyrinth
    if t+1 == len(args["labyrinth"]): # if we are at the last coordinate of dimension 1 (the time dimension)
        args["labyrinth"] += labyrinth # then we add the sequence [t0, t1, t2, t3, t4] to the labyrinth
    t += 1 # t is incremented by one unit
    return args

path = pathfinder.resolve(labyrinth, laws, ourCallback) # returns -> [(0, 1, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 1), (5, 1, 1), (6, 1, 2), (7, 1, 3), (8, 1, 4)]
```

So we have a cleaner way to solve the labyrinth. But let's detail the callback parameter :

```python
def ourCallback(args):
    print([arg for arg in args])

path = pathfinder.resolve(labyrinth, laws, ourCallback) 

# output
# -> ['labyrinth', 'laws', 'paths']
# ->             ...
# -> ['labyrinth', 'laws', 'paths']
```

Our callaback function is called before each step of resolution of the labyrinth. It receives in parameter a dict with the following keys : 

- 'labyrinth' (the maze being resolved.)
- 'laws' (the laws of the dimensions of the labyrinth.)
- 'paths' (the list of paths being calculated.)

We can access these data but we can also modify them. To do this, our callback function must return a (optional) dict with the 'labyrinth' key and its new value (same for 'laws' and 'paths').

We can also save our labyrinth in a file and reload it from the same :

```python
pathfinder.saveNarray("myLaby.laby", labyrinth)
labyrinth2 = pathfinder.loadNarray("myLaby.laby")
# labyrinth and labyrinth2 are the same
```
> pathfinder.js can use the same file format

### Javascript

Solving a two-dimensional labyrinth that changes over time is like solving a three-dimensional labyrinth (2 spatial dimensions and 1 temporal dimension) :

```javascript
const t0 = [
    [0, 0, 0, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
];

const t1 = [
    [0, 0, 1, 0, 0],
    [2, 0, 0, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
];

const t2 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
];

const t3 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0]
];

const t4 = [
    [0, 0, 1, 0, 0],
    [2, 0, 1, 0, 3],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
];

var labyrinth = [t0, t1, t2, t3, t4]; // labyrinth[t][x][y]
```

We have our three-dimensional labyrinth but we can't do :

```javascript
var path = PATHFINDER.resolve(labyrinth); // -> returns a wrong solution
```

The problem is that we have not specified that dimension 1 is a time dimension. A temporal dimension cannot be traversed in the same way as a spatial dimension : in a temporal dimension we can only move into the future and always by the same unit; that is, we must always increment the coordinates of the temporal dimension by a fixed value (in most cases by 1). 
The library has a panel of laws that define how to browse a dimension :

- PATHFINDER.FREE (default rule: the coordinate of a FREE dimension can be either incremented or decremented or remain fixed.)
- PATHFINDER.BLOCKED (the coordinate of a BLOCKED dimension always remains fixed.)
- PATHFINDER.FORWARD (the coordinate of a FORWARD dimension can be either incremented or remain fixed.)
- PATHFINDER.JUMP_FORWARD (the coordinate of a JUMP_FORWARD dimension is always incremented.)
- PATHFINDER.BACKWARD (the coordinate of a BACKWARD dimension can be either decremented or remain fixed.)
- PATHFINDER.JUMP_BACKWARD (the coordinate of a JUMP_BACKWARD dimension is always incremented.)

The JUMP_FORWARD law is perfectly adapted to run through a temporal dimension. let's specify that dimension 1 must follow this law :

```javascript
var laws = PATHFINDER.newLaw(1, PATHFINDER.JUMP_FORWARD); // here, the dimension index starts at 1 and not at 0 

// We can add a law like this for example:
// laws = PATHFINDER.newLaw(2, PATHFINDER.FORWARD, laws)
```

We can try to solve the labyrinth :

```javascript
var path = PATHFINDER.resolve(labyrinth, laws); // will return false
```

No path will be found yet we see that the labyrinth is resolvable, why ? It is simply that we arrive at the last coordinate of the first dimension (the time dimension) before having found the exit.
We can solve this problem like this :

```javascript
var labyrinth = [t0, t1, t2, t3, t4, t0, t1, t2, t3, t4]; // We repeat the transformation sequence once

var laws = PATHFINDER.newLaw(1, pathfinder.JUMP_FORWARD);

var path = PATHFINDER.resolve(labyrinth, laws); // returns -> [[0, 1, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 1], [5, 1, 1], [6, 1, 2], [7, 1, 3], [8, 1, 4]]
```
> Notice that each step of the path is represented by 3 coordinates because we have a three-dimensional labyrinth, the first coordinate is that of time.

It solves our problem, but it's not a clean way. How many times must the sequence be repeated for a more complex maze ? We can't know until we solve it. But we can add the sequence as we solve the labyrinthe thanks to the callback parameter :

```javascript
var labyrinth = [t0, t1, t2, t3, t4];
var laws = PATHFINDER.newLaw(1, PATHFINDER.JUMP_FORWARD);

var t = 0 // represents time

var ourCallback = (args) => { // our callback function
    if (t+1 == args["labyrinth"].length) { // if we are at the last coordinate of dimension 1 (the time dimension)
		args["labyrinth"] = args["labyrinth"].concat(labyrinth); // then we add the sequence [t0, t1, t2, t3, t4] to the labyrinth
	}
    t += 1; // t is incremented by one unit
	return args;
}

path = PATHFINDER.resolve(labyrinth, laws, ourCallback); // returns -> [[0, 1, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 1], [5, 1, 1], [6, 1, 2], [7, 1, 3], [8, 1, 4]]
```

So we have a cleaner way to solve the labyrinth. But let's detail the callback parameter :

```javascript
var ourCallback = (args) => {
	for (let arg of Object.keys(args)) {
		console.log(arg);
	}
}

var path = PATHFINDER.resolve(labyrinth, laws, ourCallback);

// output
// -> "labyrinth"
// -> "laws"
// -> "paths"
// ->  ...
```

Our callaback function is called before each step of resolution of the labyrinth. It receives in parameter a Object with the following keys : 

- "labyrinth" (the maze being resolved.)
- "laws" (the laws of the dimensions of the labyrinth.)
- "paths" (the list of paths being calculated.)

We can access these data but we can also modify them. To do this, our callback function must return a (optional) Object with the "labyrinth" key and its new value (same for "laws" and "paths").

We can also save our labyrinth in a file and reload it from the same :

```html
<input type="file" id="reader">
```

```javascript
var reader = document.getElementById("reader");

PATHFINDER.export(labyrinth, "nameOfFile.extesnion");
PATHFINDER.import(reader, (labyrinth, laws) => {
	//some code
})
```
> pathfinder.py can use the same file format