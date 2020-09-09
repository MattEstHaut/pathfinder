var labyrinth = [
	["#", "S", "#", "#", "#", "#", "#", "#", "#", "#"],
	["#", " ", "#", "#", "#", "#", "#", "#", "#", "#"],
	["#", " ", " ", " ", " ", " ", " ", "#", "#", "#"],
	["#", "#", "#", "#", " ", "#", " ", "#", "#", "#"],
	["#", "#", "#", "#", " ", "#", "#", "#", "#", "#"],
	["#", "#", "#", "#", " ", "#", "#", "#", "#", "#"],
	["#", "#", "#", "#", " ", " ", "#", "#", "#", "#"],
	["#", "#", "#", "#", "#", " ", " ", " ", "E", "#"],
	["#", "#", "#", " ", " ", " ", "#", "#", "#", "#"],
	["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
];

const PATHFINDER = window.PATHFINDER || {};

PATHFINDER.labyrinths = [];

PATHFINDER.export = (labyrinth) => {
	labyrinth = PATHFINDER.export_conversion(labyrinth);
	let blob = new Blob([labyrinth], {type: "text/plain"});
	let a = document.createElement("a");
	a.download = "labyrinth.lbrth";
	a.href = URL.createObjectURL(blob);
	a.dataset.downloadurl = ["text/plain", a.download, a.href].join(":");
	a.style.display = "none";
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	setTimeout(() => {URL.revokeObjectURL(a.href);}, 1500);
}

PATHFINDER.import = (input, callback = (labyrinth) => {}) => {
	input.addEventListener("change", (evt) => {
		let file = input.files[0];
		let reader = new FileReader();
		reader.addEventListener("load", (evt) => {
			let labyrinth = PATHFINDER.import_conversion(evt.target.result);
			PATHFINDER.labyrinths.push(labyrinth);
			callback(labyrinth);
		});
		reader.readAsText(file);
	});
}

PATHFINDER.import_conversion = (labyrinth) => {
	labyrinth.replace(labyrinth[2], "S");
	labyrinth.replace(labyrinth[4], "E");
	labyrinth.replace(labyrinth[6], " ");
	labyrinth.replace(labyrinth[8], "#");
	labyrinth = labyrinth.split("\n");
	labyrinth.shift();
	for (let row in labyrinth) {
		labyrinth[row] = Array.from(labyrinth[row]);
	}
	return labyrinth;
}

PATHFINDER.export_conversion = (labyrinth) => {
	let exported = "[SSEEP W#]";
	for (let row of labyrinth) {
		exported += "\n";
		for (let element of row) {
			exported += element;
		}
	}
	return exported;
}

PATHFINDER._get_cross = (center, labyrinth) => {
	var cross = [["#", "#", "#"],
				 ["#", "#", "#"],
				 ["#", "#", "#"]];
	if (center.length == 2) {
		if (center[0] > 0) {
			cross[0][1] = labyrinth[center[0]-1][center[1]];
		}
		if (center[0] < labyrinth.length-1) {
			cross[2][1] = labyrinth[center[0]+1][center[1]];
		}
		if (center[1] > 0) {
			cross[1][0] = labyrinth[center[0]][center[1]-1];
		}
		if (center[1] < labyrinth[0].length-1) {
			cross[1][2] = labyrinth[center[0]][center[1]+1];
		}
	}
	return cross;
}

PATHFINDER._copy = (path) => {
	let new_path = [];
	for (let step in path) {
		new_path.push(path[step]);
	}
	return new_path;
}

PATHFINDER._includes = (a, b) => {
	for (let ae=0; ae < a.length; ae++) {
		if (a[ae][0]==b[0] && a[ae][1]==b[1]) {
			return true;
		}
	}
	return false;
}

PATHFINDER.resolve = (labyrinth) => {
	let start = false;
	for (let row=0; row<labyrinth.length; row++) {
		for (let column=0; column<labyrinth[0].length; column++) {
			if (labyrinth[row][column] == "S") {
				start = [row, column];
			}
		}
	}
	if (!start)
		return 1;

	let paths = [["start", start]]
	let blocked = false;

	while (!blocked) {
		let n = paths.length;
		for (let p=0; p < n; p++) {
			let position = paths[p][paths[p].length-1];
			let cross = PATHFINDER._get_cross(position, labyrinth);
			let possibilities = 0;

			if (cross[0][1]==" " || cross[0][1]=="E") {
				let direction = [position[0]-1, position[1]];
				if (!PATHFINDER._includes(paths[p], direction)) {
					paths[p].push(direction);
					possibilities++;
				}
			}

			if (cross[2][1]==" " || cross[2][1]=="E") {
				let direction = [position[0]+1, position[1]];
				if (!PATHFINDER._includes(paths[p], direction)) {
					if (possibilities == 0) {
						paths[p].push(direction);
						possibilities++;
					} else {
						let copy = PATHFINDER._copy(paths[p]);
						copy[copy.length-1] = direction;
						paths.push(copy);
					}
				}
			}

			if (cross[1][0]==" " || cross[1][0]=="E") {
				let direction = [position[0], position[1]-1];
				if (!PATHFINDER._includes(paths[p], direction)) {
					if (possibilities == 0) {
						paths[p].push(direction);
						possibilities++;
					} else {
						let copy = PATHFINDER._copy(paths[p]);
						copy[copy.length-1] = direction;
						paths.push(copy);
					}
				}
			}

			if (cross[1][2]==" " || cross[1][2]=="E") {
				let direction = [position[0], position[1]+1];
				if (!PATHFINDER._includes(paths[p], direction)) {
					if (possibilities == 0) {
						paths[p].push(direction);
						possibilities++;
					} else {
						let copy = PATHFINDER._copy(paths[p]);
						copy[copy.length-1] = direction;
						paths.push(copy);
					} 
				}
			}

			if (possibilities == 0 && position.length == 2) {
				if (labyrinth[position[0]][position[1]] == "E")
					paths[p].push("end");
				else
					paths[p].push("blocked");
			}
		}

		blocked = true;
		for (let path of paths) {
			if (path[path.length-1].length == 2)
				blocked = false
		}
	}

	let solutions = [];
	let shortest = false;
	for (let path of paths) {
		if (path[path.length-1] == "end") {
			solutions.push(path);
			if (!shortest) {
				shortest = path;
			} else if (shortest.length > path.length) {
				shortest = path;
			}
		}
	}

	return {"paths": paths, "solutions": solutions, "shortest": shortest, "shortest_length": shortest.length-3};
}