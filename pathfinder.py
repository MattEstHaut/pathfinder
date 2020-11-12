#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    PATHFINDER
    ==========

    N-dimensional pathfinder algoritm module. \n
    Supports temporal dimensions.

    https://github.com/MattEstHaut/pathfinder

    Exemple :
    ---------
    >>> import pathfinder as pf
    >>> labyrinth = [[0,0,0,0,0],[2,1,0,1,0],[0,1,0,0,0],[0,1,0,1,0],[0,1,3,1,0]]
    >>> pf.resolve(labyrinth)
    [(1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
"""

# constantes : types de case du labyrinthe
PATH     = 0
WALL     = 1
START    = 2 # un seul point de départ est autorisé
END      = 3 # plusieurs sorties sont autorisées
BANNED   = 4 # les cases déjà parcourues sont bannies (par défaut)

# constantes : manières de parcourir une dimension
FREE           = 0 # bidirectionelle (la valeur de la coordonnée peut être incrémentée et décrémentée ou rester statique)
BLOCKED        = 1 # statique (la coordonnée dans une dimension suivant la loi BLOCKED est constante)
FORWARD        = 2 # unidirectionelle + (la valeur de la coordonnée peut être incrémentée ou rester statique)
JUMP_FORWARD   = 3 # unidirectionelle - (la valeur de la coordonnée peut être décrémentée ou rester statique)
BACKWARD       = 4 # force l'incrémentation de la coordonnée (utile pour les dimensions temporelles)
JUMP_BACKWARD  = 5 # force la décrémentation de la coordonnée (utile pour les dimensions temporelles)


def getDimension(labyrinth: list) -> int:
    """
        getDimension
        ============

        Description :
        -------------
        Returns the number of dimension of labyrinth.

        Example :
        ---------
        >>> getDimension([[0,0],[0,0]])
        2

        Parameters :
        ------------
            labyrinth (list): n-dimensional array of int.
        
        Returns :
        ---------
            int: the number of dimension.
    """

    if type(labyrinth) is list: # si labyrinth est de type list -> retourne 1 + le nombre de dimension de labyrinth[0]
        return 1 + getDimension(labyrinth[0])
    return 0 # si labyrinth n'est pas de type list -> retourne 0, le nombre de dimension d'un nombre


def findStart(labyrinth: list, d=None, n=0, c=()) -> tuple:
    """
        findStart
        =========

        Description
        -----------
        Returns the coordinates of the starting point of labyrinth.

        Exemple :
        ---------
        >>> findStart([[0,2],[0,0]])
        (0,1)

        Parameters :
        ------------
            labyrinth (list): n-dimensional array of int.
        
        Returns :
        ---------
            tuple of int: the the coordinates of the starting point.
    """

    # obtient le nombre de dimension
    if d is None: d = getDimension(labyrinth)

    # parcourt toutes les coordonnées jusqu'à trouver le point de départ

    if n + 1 == d: # condition d'arrêt : on est à la dernière dimension
        for i in range(len(labyrinth)):
            if labyrinth[i] == START:
                return c + (i,)
        return None

    for i in range(len(labyrinth)):
        j = findStart(labyrinth[i], d, n+1, c+(i,))
        if j is not None:
            return j
    

def getAdjacentCoordinates(center: tuple, laws={}, force=False) -> list:
    """
        getAdjacentCoordinates
        ======================

        Description
        -----------
        Returns all adjacent coordinates of a point.

        Exemples :
        ----------
        >>> getAdjacentCoordinates((2,10))
        [(2,10),(1,10),(3,10),(2,9),(2,11)]
        >>> getAdjacentCoordinates((2,10), force=True)
        [(1,10),(3,10),(2,9),(2,11)]
        >>> getAdjacentCoordinates((2,10), laws={1: BLOCKED})
        [(2,9),(2,11)]

        Parameters :
        ------------
            center (tuple of int): coordinates.
            laws (dict): see newLaw function for details.
            force (bool): do not include the center coordinates if True.
        
        Returns :
        ---------
            list of tuple of int: a list of coordinates.
    """

    laws = laws.copy() # fait une copy de laws pour ne pas modifier le dictionnaire d'origine

    for d in range(len(center)):
        if d+1 in laws: 
            if laws[d+1] == JUMP_FORWARD: # si laws indique que la dimension d suit la loi JUMP_FORWARD -> incrémente la coordonnée de center de cette dimension
                center = center[:d]+(center[d]+1,)+center[d+1:]
                laws[d+1] = BLOCKED # bloque temporairement la dimension
                continue
            if laws[d+1] == JUMP_BACKWARD: # si laws indique que la dimension d suit la loi JUMP_BACKWARD -> décrémente la coordonnée de center de cette dimension
                center = center[:d]+(center[d]-1,)+center[d+1:]
                laws[d+1] = BLOCKED # bloque temporairement la dimension
                continue

    l = [] # l est la liste des coordonnées adjacentes à center
    if not force: # si force=False -> ajoute center à l
        l.append(center)

    for c in range(len(center)):
        if c+1 in laws:
            if laws[c+1] == BLOCKED: # si la dimension c suit la loi BLOCKED -> passe à la dimension suivante
                continue
            if laws[c+1] == FORWARD: # si la dimension c suit la loi FORWARD -> ajoute le tuple identique à center avec la coordonnée à la dimension c incrémentée
                s = center[c]+1
                l += [center[:c]+(s,)+center[c+1:]]
                continue
            if laws[c+1] == BACKWARD: # si la dimension c suit la loi BACKWARD -> ajoute le tuple identique à center avec la coordonnée à la dimension c décrémentée
                i = center[c]-1
                l += [center[:c]+(i,)+center[c+1:]]
                continue
        i, s = center[c]-1, center[c]+1 # si la dimension c suit la loi FREE (par defaut) -> ajoute les tuple identiques
                                        #  à center avec la coordonnée à la dimension c incrémentée et décrémentée
        l += [center[:c]+(i,)+center[c+1:]]
        l += [center[:c]+(s,)+center[c+1:]]
    return l
    

def isLegalCoordinate1D(x: int, l: int) -> bool:
    """
        isLegalCoordinate1D
        ===================

        Description :
        -------------
        Returns True if x is in a dimension of length l, else return False.

        Exemples :
        ----------
        >>> isLegalCoordinate1D(2,10)
        True
        >>> isLegalCoordinate1D(16,10)
        False
        >>> isLegalCoordinate1D(-4,10)
        False

        Parameters :
        ------------
            x (int): coordinate.
            l (int): length of the dimension.
        
        Returns :
        ---------
            bool: True if x is in a dimension of length l, else False.
    """

    # la coordonnée x est légale si dimension[x] existe
    return (x >= 0 and x < l)


def isLegalCoordinate(c: tuple, labyrinth: list) -> bool:
    """
        isLegalCoordinate
        =================

        Description :
        -------------
        Returns True if c is a legal coordinate, else return False.

        Exemples :
        ----------
        >>> isLegalCoordinate((1,0),[[0,0],[0,0]])
        True
        >>> isLegalCoordinate((1,5),[[0,0],[0,0]])
        False
        >>> isLegalCoordinate((-1,1),[[0,0],[0,0]])
        False

        Parameters :
        ------------
            c (tuple of int): coordinates.
            labyrinth (list): n-dimensional array of int.
        
        Returns :
        ---------
            bool: True if c is in labyrinth, else False.
    """

    for d in c: # vérifie que toute les coordonnées sont dans légales leurs dimensions respectives
        if not isLegalCoordinate1D(d, len(labyrinth)):
            return False
        labyrinth = labyrinth[d] # passe à la dimension suivante
    return True


def getAdjacents(center: tuple, labyrinth: list, laws={}) -> list:
    """
        getAdjacents
        ============

        Description :
        -------------
        Returns all legal adjacent coordinates of a point.

        Exemples :
        ----------
        >>> getAdjacents((1,0),[[0,0],[0,0]])
        [(1,0), (0,0), (1,1)]
        >>> getAdjacents((1,0),[[0,0],[0,0]], laws={1: FORWARD})
        [(1,0), (1,1)]

        Parameters :
        ------------
            center (tuple of int):  coordinates.
            labyrinth (list): n-dimensional array of int.
            laws (dict): see newLaw function for details.
        
        Returns :
        ---------
            list of tuple of int: a list of coordinates. 
    """

    adjacentCoordinates = getAdjacentCoordinates(center, laws) # obtient les coordonnées adjacentes
    adjacents = []
    for c in adjacentCoordinates:
        if isLegalCoordinate(c, labyrinth): # si les coordonnées sont légales -> les ajoute à adjacents
            adjacents.append(c)
    return adjacents


def getCase(center: tuple, labyrinth: list) -> int:
    """
        getCase
        =======

        Description :
        -------------
        Returns the value of the case at center in labyrinth.

        Exemple :
        ---------
        >>> getCase((1,0),[[0,1],[2,3]])
        2

        Parameters :
        ------------
            center (tuple of int): coordinates.
            labyrinth (list): n-dimensional array of int.
        
        Returns :
        ---------
            int: value of the case.
    """

    for x in center: # revient à faire labyrinth[center1][center2][center3] ... [centern-1][centern] avec n le nombre de dimension de center
        labyrinth = labyrinth[x]
    return labyrinth


def getCases(centers: list, labyrinth: list) -> list:
    """"
        getCases
        ========

        Description:
        ------------
        Returns all the values of the cases at center* in labyrinth.

        Exemple :
        ---------
        >>> getCases([(1,0),(0,0)],[[0,1],[2,3]])
        [2,0]

        Parameters :
        ------------
            centers (list of tuple of int): list of coordinates.
            labyrinth (list): n-dimensional array of int.
        
        Returns :
        ---------
            list of int: values of the cases.
    """
    
    return [getCase(d, labyrinth) for d in centers]


def newLaw(d: int, law: int, laws={}) -> dict:
    """
        newLaw
        ======

        Description :
        -------------
        Adds a law to dimension d.
        Returns dictionary of laws.

        Laws :
        - FREE
        - BLOCKED
        - FORWARD
        - JUMP_FORWARD (useful for temporal dimensions)
        - BACKWARD
        - JUMP_BACKWARD (useful for temporal dimensions)

        newLaw("NO_BAN", True) => disable banishment of visited cases, useful for temporal dimensions.

        WARNING : newLaw("NO_BAN", True) significantly increases temporal complexity.

        Exemples :
        ----------
        >>> laws = newLaw(2, BLOCKED)
        >>> laws
        {2: 1}
        >>> laws = newLaw(4, FORWARD, laws)
        >>> laws
        {2: 1, 4: 2}

        Parameters :
        ------------
            d (int): dimension (begin at 1 not 0).
            law (int): law value.
            laws (dict): existing laws.
        
        Returns :
        ---------
            dict: new laws.
    """

    laws[d] = law
    return laws


def banCase(case: tuple, labyrinth: list) -> None:
    """
        banCase
        =======

        Description :
        -------------
        Bans a case of coordinates case of labyrinth.

        Exemple :
        ---------
        >>> labyrinth = [[0,1], [1,0]]
        >>> banCase((1,0), labyrinth)
        >>> labyrinth
        [[0,1], [4,0]]

        Parameters :
        ------------
            case (tuple of int): coordinates of case.
            labyrinth (list): n-dimensional array of int.
    """

    if len(case) == 1:
        labyrinth[case[0]] = BANNED
        return None

    banCase(case[1:], labyrinth[case[0]])
    # revient à faire labyrinth[case1][case2][case3] ... [casen-1][casen] = BANNED avec n le nombre de dimension de case

def appendPath(paths: list, labyrinth: list, laws={}) -> (list, bool):
    """
        appendPath
        ==========

        Description :
        -------------
        Extends all the paths of a stage.

        - remove obsolete paths.
        - duplicates the paths that separate.
        - ban visited cases (see newLaw function to disable case banishment).

        Parameters :
        ------------
            paths (list of tuple of int): list of paths.
            labyrinth (list): n-dimensional array of int.
            laws (dict): laws.

        Returns :
        ---------
            list of tuple of int: if the end has been reached.
            list of list of tuple of int: if the end has not been reached.
            bool: True if end has been reached, else False.
        /!\\ WARNING : the return is (list of tuple of int, True) or (list of list of tuple of int, False).
    """

    noBan = False # determine si la loi NO_BAN est activée
    if "NO_BAN" in laws:
        noBan = laws["NO_BAN"]

    newPaths = [] # contiendra les nouveaux chemins et ceux mis à jour
    for path in paths:
        directions = getAdjacents(path[-1], labyrinth, laws) # obtient les coordonnées des cases adjacentes suivant les lois
        cases = getCases(directions, labyrinth) # obtient les valeurs des cases aux coordonnées de directions
        if END in cases: # si la fin a été trouvée -> retourne le chemin et True
            path.append(directions[cases.index(END)])
            return path, True

        for d in range(len(directions)): # si non -> calcule des chemins découlant de path
            if cases[d] == PATH: # si la case est un chemin -> on ajoute un nouveau chemin identique avec en plus les coordonnées de la dernière case chemin
                newPaths.append(path.copy())
                newPaths[-1].append(directions[d])
                if not noBan: # si le bannissement des cases visitées n'est pas désactivé -> bannit la case
                    banCase(directions[d], labyrinth)

    return newPaths, False # retourne les nouveaux chemins et False


def defaultCallback(arg: {}) -> None:
    """
        Does nothing ( °_°')
    """

    # cette fonction est une fonction inutile utilisée comme fonction par défaut dans resolve()
    return None


def resolve(labyrinth: list, laws={}, callback=defaultCallback) -> list:
    """
        resolve
        =======

        Description :
        -------------
        Resolves n-dimensional labyrinth.

        Exemple :
        ---------
        >>> labyrinth = [[2,1,3], [0,1,0], [0,0,0]]
        >>> resolve(labyrinth)
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)]

        Labyrinth parameter :
        ---------------------
        Labyrinth is n-dimensional array of int. \n
        
            PATH     = 0
            WALL     = 1
            START    = 2
            END      = 3
            BANNED   = 4

        Laws parameter :
        -----------------
        See newLaw function documentation. \n
        Laws is a dict of this form : \n
        {dimensionNumber: law, dimensionNumber: law, ...} \n
        /!\ WARNING: dimensionNumber begin at 1 not 0. \n
        If no law is explicit for a dimension, it will by default follow the FREE law. \n

        Availible laws :
        - FREE
        - BLOCKED
        - FORWARD
        - JUMP_FORWARD (useful for temporal dimensions)
        - BACKWARD
        - JUMP_BACKWARD (useful for temporal dimensions)

        If laws["NO_BAN"] is True => disable banishment of visited cases, useful for temporal dimensions. \n
        /!\ WARNING : set NO_BAN to True significantly increases temporal complexity.

        Callback parameter :
        --------------------
        The callback function is called at each step as well : \n
        callback({"labyrinth": labyrinth, "laws": laws, "paths": paths}) \n
        paths is a list of possible correct routes (list of list of tuple of int) \n
        If the return of callback is a dict with keys "labyrinth", "laws" or "paths" -> the value of the original variable will be modified.

        Parameters :
        ------------
            labyrinth (list): n-dimensional array of int.
            laws (dict): laws.
            callback (function): function that executes at each step.

        Returns:
        --------
            list of tuple of int: path (if the end has not been reached -> return None)
    """

    paths = [[findStart(labyrinth)]] # creer une list d'un seul chemin contenenant un seul tuple de coordonnées : celles du point de départ
    end = False
    while not end: # tant que la sortie n'a pas été trouvée ou que tout les chemins ont été visités
        arg = callback({"labyrinth": labyrinth, "laws": laws, "paths": paths}) # appel de la fonction callback
        if type(arg) is dict: # mise à jour potentiel de labyrinth, laws et paths
            if "labyrinth" in arg: labyrinth = arg["labyrinth"]
            if "laws" in arg: laws = arg["laws"]
            if "paths" in arg: paths = arg["paths"]

        paths, end = appendPath(paths, labyrinth, laws) # met à jours paths
        if len(paths) == 0: # si tout les chemins ont été visités et qu'il n'y pas de chemin qui mène à la sortie -> retourne None
            return None

    return paths


def narrayShape(narray: list):
    """
        narrayShape
        =======

        Description :
        -------------
        Returns the shape of narray.

        Exemple :
        ---------
        >>> narrayShape([[1,2], [3,4], [4,5]])
        [3, 2]

        Parameters :
        ------------
            narray (list): n-dimensional array of int.

        Returns:
        --------
            list of int: shape of narray.
    """

    if type(narray) is not list:
        return []
    return [len(narray)] + narrayShape(narray[0])
    # revient à faire [len(narray), len(narray[0]), len(array[0][0]), ... ]
    

def narrayFlatten(narray: list):
    """
        narrayFlatten
        =======

        Description :
        -------------
        Flattens a n-dimensional array to unidimensional array.

        Exemple :
        ---------
        >>> narrayFlatten([[1,2], [3,4], [4,5]])
        [1, 2, 3, 4, 4, 5]

        Parameters :
        ------------
            narray (list): n-dimensional array of int.

        Returns:
        --------
            list of int: unidimensional array.
    """

    if type(narray[0]) is not list:
        return narray
    fnarray = []
    for a in narray:
        fnarray += narrayFlatten(a)
    return fnarray


def narrayUnflatten(array: list, shape: list):
    """
        narrayUnlatten
        ==============

        Description :
        -------------
        Gives the desired shape to array.

        Exemple :
        ---------
        >>> narrayUnlatten([1, 2, 3, 4, 4, 5], [3, 2])
        [[1,2], [3,4], [4,5]]

        Parameters :
        ------------
            array (list of int): unidimensional array of int.
            shape (list of int): the shape to give to array.

        Returns:
        --------
            list: n-dimensional array of int.
    """

    if len(shape) == 1:
        return array
    s = len(array)//shape[0]
    narray = []
    for i in range(0, len(array), s):
        subarray = [array[j] for j in range(i, i+s)]
        narray.append(narrayUnflatten(subarray, shape[1:]))
    return narray


def narray2str(narray: list, laws={}) -> str:
    """
        narray2str
        ==========

        Description :
        -------------
        Stringify narray and laws.

        Exemple :
        ---------
        >>> narray2str([[1, 2],[3, 4],[4, 5]])
        3:2:
        0:0:
        1:2:3:4:4:5:
        0

        Parameters :
        ------------
            narray (list): n-dimensional array of int.
            laws (dict): laws.

        Returns:
        --------
            str: stringified narray and laws.
    """

    shape = narrayShape(narray)
    array = narrayFlatten(narray)
    ss = sl = sa = ""
    for d in shape:
        ss += str(d) + ":"
    for l in range(len(shape)):
        if l+1 in laws:
            sl += str(laws[l+1]) + ":"
        else:
            sl += str(FREE) + ":"
    for v in array:
        sa += str(v) + ":" 
    sb = "0"
    if "NO_BAN" in laws:
        if laws["NO_BAN"]:
            sb = "1"
    return ss + "\n" + sl + "\n" + sa + "\n" + sb


def str2narray(data: str) -> (list, dict):
    """
        str2narray
        ==========

        Description :
        -------------
        Convert string to n-dimensional array and laws.

        Exemple :
        ---------
        >>> s = "3:2:\n0:0:\n1:2:3:4:4:5:\0"
        >>> a, l = str2narray(s)
        >>> a
        [[1, 2],[3, 4],[4, 5]]
        >>> l
        {1: 0, 2: 0, "NO_BAN": false}

        Parameters :
        ------------
            data (str): stringified narray and laws.

        Returns:
        --------
            (list, dict): n-dimensional array and laws.
    """

    data = data.split("\n")
    shape = [int(x) for x in data[0].split(":")[:-1]]
    laws = [int(x) for x in data[1].split(":")[:-1]]
    array = [int(x) for x in data[2].split(":")[:-1]]
    narray = narrayUnflatten(array, shape)
    dlaws = {}
    for l in range(len(laws)):
        dlaws[l+1] = laws[l]
    dlaws["NO_BAN"] = int(data[3][0])
    return narray, dlaws
        
def saveNarray(path: str, narray: list, laws={}) -> None:
    """
        saveNarray
        ==========

        Description :
        -------------
        Save narray and laws in a file.

        Parameters :
        ------------
            path (str): file path.
            narray (list): n-dimensional array.
            laws (dict): laws.
    """

    stringifiedNArray = narray2str(narray, laws)
    save = open(path, "w")
    save.write(stringifiedNArray)
    save.close()

def loadNarray(path: str) -> (list, dict):
    """
        loadNarray
        ==========

        Description :
        -------------
        Read narray and laws from a file.

        Parameters :
        ------------
            path (str): file path.

        Returns:
        --------
            (list, dict): n-dimensional array and laws.
    """
    
    save = open(path, "r")
    data = save.read()
    save.close()
    return str2narray(data)