/**
 * PATHFINDER
 * ==========
 *
 * N-dimensional pathfinder algoritm module.
 * Supports temporal dimensions.
 *
 * https://github.com/MattEstHaut/pathfinder
 */

const PATHFINDER = window.PATHFINDER || {};

PATHFINDER.PATH     = 0;
PATHFINDER.WALL     = 1;
PATHFINDER.START    = 2;
PATHFINDER.END      = 3;
PATHFINDER.BANNED   = 4;
PATHFINDER.SOLUTION = 5;

PATHFINDER.FREE          = 0;
PATHFINDER.BLOCKED       = 1;
PATHFINDER.FORWARD       = 2;
PATHFINDER.JUMP_FORWARD  = 3;
PATHFINDER.BACKWARD      = 4;
PATHFINDER.JUMP_BACKWARD = 5;


/**
 * getDimension
 * ============
 * 
 * Description :
 * -------------
 * Returns the number of dimension of labyrinth.
 * @param   {Array}  labyrinth N-dimensional array of int.
 * @param   {Number} d    
 * @returns {Number}           The number of dimension.
 */
PATHFINDER.getDimension = (labyrinth, d=0) => {
    if (typeof(labyrinth) != "number") {
        return 1 + PATHFINDER.getDimension(labyrinth[0], d);
    }
    return d;
}

/**
 * findStart
 * =========
 * 
 * Description :
 * -------------
 * Returns the coordinates of the starting point of labyrinth.
 * @param   {Array}  labyrinth N-dimensional array of int.
 * @param   {Number} d 
 * @param   {Number} n 
 * @param   {Number} c
 * @returns {Array}            Coordinates of starting point.
 */
PATHFINDER.findStart = (labyrinth, d=0, n=0, c=[]) => {
    if (d==0) {
        d = PATHFINDER.getDimension(labyrinth);
    }

    if (n+1 == d) {
        for (let i=0; i<labyrinth.length; i++) {
            if (labyrinth[i] == PATHFINDER.START) {
                return c.concat([i]);
            }
        }
        return [];
    }

    for (let i=0; i<labyrinth.length; i++) {
        let j = PATHFINDER.findStart(labyrinth[i], d, n+1, c.concat([i]));
        if (j != -1) {
            return j;
        }
    }
}

/**
 * getAdjacentCoordinates
 * ======================
 * 
 * Description :
 * -------------
 * Returns all adjacent coordinates of a point.
 * @param   {Array}   center Coordinates.
 * @param   {Object}  laws   See documentation for details.
 * @param   {boolean} force  Do not include the center coordinates if true.
 * @returns {Array}          Array of coordinates.
 */
PATHFINDER.getAdjacentCoordinates = (center, laws={}, force=false) => {
    laws = [...laws];

    for (let d=0; d<center.length; d++) {
        if (laws.hasOwnProperty(d+1)) {
            switch (laws[d+1]) {
                case PATHFINDER.JUMP_FORWARD:
                    center[d]++;
                    laws[d+1] = PATHFINDER.BLOCKED;
                    break;
                case PATHFINDER.JUMP_BACKWARD:
                    center[d]--;
                    laws[d+1] = PATHFINDER.BLOCKED;
                    break;
                default:
                    break;
            }
        }
    }

    let l = []; let i; let s; let ci; let cs;
    if (!force) {
        l.push(center);
    }

    for (let c=0; c<center.length; c++) {
        if (laws.hasOwnProperty(c+1)) {
            switch (laws[c+1]) {
                case PATHFINDER.BLOCKED:
                    break;
                case PATHFINDER.FORWARD:
                    s = center[c]+1;
                    cs = [...center];
                    cs[c] = s;
                    l.push(cs);
                    break;
                case PATHFINDER.BACKWARD:
                    i = center[c]-1;
                    ci = [...center];
                    ci[c] = i;
                    l.push(ci);
                    break;
                default:
                    break;
            }
        } else {
            i = center[c]-1;
            s = center[c]+1;
            ci = [...center];
            cs = [...center];
            ci[c] = i;
            cs[c] = s;
            l.push(ci);
            l.push(cs);
        }
    }
    return l;
}

/**
 * isLegalCoordinate1D
 * ===================
 * 
 * Description :
 * -------------
 * Returns true if x is in a dimension of length l, else return false.
 * @param   {Number}  x Coordinate.
 * @param   {Number}  l Length of dimension.
 * @returns {Boolean}   true if x is in a dimension of length l, else false.
 */
PATHFINDER.isLegalCoordinate1D = (x, l) => {
    return (x>=0 && x<l);
}

/**
 * isLegalCoordinates
 * ==================
 * 
 * Description :
 * -------------
 * Returns true if c is a legal coordinate, else return false.
 * @param   {Array}   c         Coordinates.
 * @param   {Array}   labyrinth N-dimensional array of int.
 * @returns {boolean}           true if c is a legal coordinate, else false.
 */
PATHFINDER.isLegalCoordinates = (c, labyrinth) => {
    for (let d of c) {
        if (!PATHFINDER.isLegalCoordinate1D(d, labyrinth.length)) {
            return false;
        }
        labyrinth = labyrinth[d];
    }
    return true;
}

/**
 * getAdjacents
 * ============
 * 
 * Description :
 * -------------
 * Returns all legal adjacent coordinates of a point.
 * @param   {Array}  center    Coordinates.
 * @param   {Array}  labyrinth N-dimensional array of int.
 * @param   {Object} laws      See documentation for details.
 * @returns {Array}            Array of coordinates.
 */
PATHFINDER.getAdjacents = (center, labyrinth, laws={}) => {
    adjacentCoordinates = PATHFINDER.getAdjacentCoordinates(center, laws);
    adjacents = [];
    for (let c of adjacentCoordinates) {
        if (PATHFINDER.isLegalCoordinates(c, labyrinth)) {
            adjacents.push(c);
        }
    }
    return adjacents;
}

/**
 * getCase
 * =======
 * 
 * Description :
 * -------------
 * Returns the value of the case at center in labyrinth.
 * @param   {Array} center    Coordinates.
 * @param   {Array} labyrinth N-dimensional array of int.
 * @returns {Number}          Value of the case.
 */
PATHFINDER.getCase = (center, labyrinth) => {
    for (let x of center) {
        labyrinth = labyrinth[x];
    }
    return labyrinth;
}

/**
 * getCases
 * ========
 * 
 * Description :
 * -------------
 * Returns all the values of the cases at center* in labyrinth.
 * @param   {Array} centers   Array of coordinates.
 * @param   {Array} labyrinth N-dimensional array of int.
 * @returns {Array}           Values of the cases.
 */
PATHFINDER.getCases = (centers, labyrinth) => {
    let cases = [];
    for (let d of centers) {
        cases.push(PATHFINDER.getCase(d, labyrinth));
    }
    return cases;
}


/**
 * newLaw
 * ======
 * 
 * Description :
 * -------------
 * adds a law to dimension d.
 * returns dictionary of laws.
 * 
 * Laws :
 * ------
 *      - FREE
 *      - BLOCKED
 *      - FORWARD
 *      - JUMP_FORWARD (useful for temporal dimensions)
 *      - BACKWARD
 *      - JUMP_BACKWARD (useful for temporal dimensions)
 * 
 * PATHFINDER.newLaw("NO_BAN", true) => disable banishment of visited cases, useful for temporal dimensions.
 * 
 * WARNING : PATHFINDER.newLaw("NO_BAN", true) significantly increases temporal complexity.
 * 
 * @param   {Number} d    Dimension (begin at 1 not 0).
 * @param   {Number} law  Law value.
 * @param   {Object} laws Existing laws.
 * @returns {Object}      New laws. 
 */
PATHFINDER.newLaw = (d, law, laws={}) => {
    laws[d] = law;
    return laws;
}

/**
 * banCase
 * =======
 * 
 * Description :
 * -------------
 * Bans a case of coordinates case of labyrinth.
 * @param {Array} c         Coordinates of case.
 * @param {Array} labyrinth N-dimensional array of int.
 */
PATHFINDER.banCase = (c, labyrinth) => {
    if (c.length == 1) {
        labyrinth[c[0]] = PATHFINDER.BANNED;
        return;
    }
    let ct = [...c];
    ct.shift();
    PATHFINDER.banCase(ct, labyrinth[c[0]]);
}

/**
 * appendPath
 * ==========
 * 
 * Description :
 * -------------
 * Extends all the paths of a stage.
 * 
 * - remove obsolete paths.
 * - duplicates the paths that separate.
 * - ban visited cases (see newLaw function to disable case banishment).
 * 
 * Parameters :
 * ------------
 * @param   {Array} paths     Array of paths.
 * @param   {Array} labyrinth N-dimensional array of int.
 * @param   {Object} laws     See newLaws function for details.
 * @returns {Array}           (path||paths, bool end?).
 */
PATHFINDER.appendPath = (paths, labyrinth, laws={}) => {
    let newPaths = [];
    let directions; let cases;

    let noBan = false;
    if (laws.hasOwnProperty("NO_BAN")) {
        noBan = laws["NO_BAN"];
    }

    for (let path of paths) {
        directions = PATHFINDER.getAdjacents(path[path.length-1], labyrinth, laws);
        cases = PATHFINDER.getCases(directions,labyrinth);
        if (cases.includes(PATHFINDER.END)) {
            path.push(directions[cases.indexOf(PATHFINDER.END)]);
            return [path, true];
        }

        for (let d=0; d<directions.length; d++) {
            if (cases[d] == PATHFINDER.PATH) {
                newPaths.push([...path]);
                newPaths[newPaths.length-1].push(directions[d]);
                if (!noBan) {
                    PATHFINDER.banCase(directions[d], labyrinth);
                }
            }
        }
    }

    return [newPaths, false];
}

/**
 * resolve
 * =======
 * 
 * Description :
 * -------------
 * resolves n-dimensional labyrinth.
 * 
 * Labyrinth is n-dimensional array of int.
 * - PATH     = 0
 * - WALL     = 1
 * - START    = 2
 * - END      = 3
 * - BANNED   = 4
 * - SOLUTION = 5
 * 
 * Laws is a Object of this form : {dimensionNumber: law, dimensionNumber: law, ...};
 * If no law is explicit for a dimension, it will by default follow the FREE law.
 * 
 * /!\ WARNING: dimensionNumber begin at 1 not 0.
 * 
 * Availible laws :
 * - FREE
 * - BLOCKED
 * - FORWARD
 * - JUMP_FORWARD (useful for temporal dimensions)
 * - BACKWARD
 * - JUMP_BACKWARD (useful for temporal dimensions)
 * 
 * PATHFINDER.newLaw("NO_BAN", true) => disable banishment of visited cases, useful for temporal dimensions.
 * 
 * WARNING : PATHFINDER.newLaw("NO_BAN", true) significantly increases temporal complexity.
 * 
 * The callback function is called at each step as well : callback({"labyrinth": labyrinth, "laws": laws, "paths": paths});
 * 
 * paths is a list of possible correct routes.
 * If the return of callback is a dict with keys "labyrinth", "laws" or "paths" -> the value of the original variable will be modified.
 * 
 * Parameters :
 * ------------
 * @param   {Array} labyrinth    N-dimensional array of int.
 * @param   {Object} laws        Laws (see newLaws function for details).
 * @param   {Function} callback  Function that executes at each step.
 * @returns {Array}              Path (if the end has not been reached -> return false).
 */
PATHFINDER.resolve = (labyrinth, laws={}, callback=()=>{}) => {
    let paths = [[PATHFINDER.findStart(labyrinth)]];
    let end = false;
    let arg; let np1;
    while (!end) {
        arg = callback({"labyrinth": labyrinth, "laws": laws, "paths": paths});
        if (typeof(arg) == "object") {
            if (Object.keys(arg).includes("labyrinth")) {
                labyrinth = arg["labyrinth"];
            }
            if (Object.keys(arg).includes("laws")) {
                laws = arg["laws"];
            }
            if (Object.keys(arg).includes("paths")) {
                paths = arg["paths"];
            }
        }

        np1 = PATHFINDER.appendPath(paths, labyrinth, laws);
        end = np1[1];
        paths = np1[0];
        if (paths.length == 0) {
            return false;
        }
    }

    return paths;
}

/**
 * narrayShape
 * ===========
 * 
 * Description :
 * -------------
 * Returns the shape of narray.
 * @param   {Array} narray N-dimensional array of int.
 * @returns {Array}        Array of int: shape of narray.
 */
PATHFINDER.narrayShape = (narray) => {
    if (typeof(narray) == "number") {
        return [];
    }
    return [narray.length].concat(PATHFINDER.narrayShape(narray[0]));
}

/**
 * narrayFlatten
 * =============
 * 
 * Description :
 * -------------
 * Flattens a n-dimensional array to unidimensional array.
 * @param   {Array} narray N-dimensional array of int.
 * @returns {Array}        Unidimensional array.
 */
PATHFINDER.narrayFlatten = (narray) => {
    if (typeof(narray[0]) == "number") {
        return narray;
    }
    let fnarray = [];
    for (let a of narray) {
        fnarray = fnarray.concat(PATHFINDER.narrayFlatten(a));
    }
    return fnarray;
}

/**
 * narrayUnflatten
 * ===============
 * 
 * Description :
 * -------------
 * Gives the desired shape to array.
 * @param   {Array} array Unidimensional array of int.
 * @param   {Array} shape The shape to give to array.
 * @returns {Array}       N-dimensional array of int.
 */
PATHFINDER.narrayUnflatten = (array, shape) => {
    if (shape.length == 1) {
        return array;
    }
    let s = array.length/shape[0]
    let narray = []; let subarray;
    let mshape;
    for (let i=0; i<array.length; i+=s) {
        subarray = [];
        for (let j=i; j<i+s; j++) {
            subarray.push(array[j]);
        }
        mshape = [...shape];
        mshape.shift();
        narray.push(PATHFINDER.narrayUnflatten(subarray, mshape));
    }
    return narray;
}

/**
 * narray2str
 * ==========
 * 
 * Description :
 * -------------
 * Stringify narray and laws.
 * @param   {Array}  narray N-dimensional array of int.
 * @param   {Object} laws   laws
 * @returns {String}        Stringified narray and laws.
 */
PATHFINDER.narray2str = (narray, laws={}) => {
    let shape = PATHFINDER.narrayShape(narray);
    let array = PATHFINDER.narrayFlatten(narray);
    let ss = "";
    let sl = "";
    let sa = "";
    for (let d of shape) {
        ss += String(d) + ":";
    }
    for (let l=0; l<shape.length; l++) {
        if (Object.keys(laws).includes(l+1)) {
            sl += String(laws[l+1]) + ":";
        } else {
            sl += String(PATHFINDER.FREE) + ":";
        }
    }
    for (let v of array) {
        sa += String(v) + ":";
    }
    let sb = "0";
    if (Object.keys(laws).includes("NO_BAN")) {
        if (laws["NO_BAN"]) {
            sb = "1";
        }
    }
    return ss + "\n" + sl + "\n" + sa + "\n" + sb;
}

/**
 * str2narray
 * ==========
 * 
 * Description :
 * -------------
 * Convert string to n-dimensional array and laws.
 * @param   {String}  data Stringified narray and laws.
 * @returns {Array}        N-dimensional array and laws
 */
PATHFINDER.str2narray = (data) => {
    data = data.split("\n");
    let shape = []; let laws = []; let array = [];
    let tmp_data = data[0].split(":");
    tmp_data.pop();
    for (let x of tmp_data) {
        shape.push(parseInt(x));
    }
    tmp_data = data[1].split(":");
    tmp_data.pop();
    for (let x of tmp_data) {
        laws.push(parseInt(x));
    }
    tmp_data = data[2].split(":");
    tmp_data.pop();
    for (let x of tmp_data) {
        array.push(parseInt(x));
    }
    let narray = PATHFINDER.narrayUnflatten(array, shape);
    let dlaws = {};
    for (let l=0; l<laws.length; l++) {
        dlaws[l+1] = laws[l];
    }
    dlaws["NO_BAN"] = parseInt(data[3][0]);
    return [narray, dlaws];
}

/**
 * export
 * ======
 * 
 * Description :
 * -------------
 * Save narray and laws in a file.
 * @param {Array}  narray N-dimensional array.
 * @param {String} name   The name of file.
 * @param {Object} laws   Laws.
 */
PATHFINDER.export = (narray, name, laws={}) => {
    stringifiedNArray = PATHFINDER.narray2str(narray, laws);
    let blob = new Blob([stringifiedNArray], {type: "text/plain"});
    let a = document.createElement("a");
	a.download = name;
	a.href = URL.createObjectURL(blob);
	a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
	a.style.display = "none";
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	setTimeout(() => {URL.revokeObjectURL(a.href);}, 1500);
}

/**
 * import
 * ======
 * 
 * Description :
 * -------------
 * Read narray and laws from a file.
 * @param {Object}   input    HTML input.
 * @param {Function} callback Callback.
 */
PATHFINDER.import = (input, callback=(labyrinth, laws) => {}) => {
    input.addEventListener("change", (evt) => {
		let file = input.files[0];
		let reader = new FileReader();
		reader.addEventListener("load", (evt) => {
            let data = PATHFINDER.str2narray(evt.target.result);
			callback(data[0], data[1]);
		});
		reader.readAsText(file);
	});
}