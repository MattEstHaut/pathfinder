const PATHFINDER = window.PATHFINDER || {};

PATHFINDER.labyrinths = [];

PATHFINDER.convert_labyrinth = (labyrinth, configuration) => {
	for (let column in labyrinth) {
		for (let row in labyrinth[column]) {
			if (labyrinth[column][row] == configuration.path)
				labyrinth[column][row] = 0;
			if (labyrinth[column][row] == configuration.wall)
				labyrinth[column][row] = 1;
			if (labyrinth[column][row] == configuration.start)
				labyrinth[column][row] = 2;
			if (labyrinth[column][row] == configuration.end)
				labyrinth[column][row] = 3;
		}
	}
	return labyrinth;
}

PATHFINDER.find_start = (labyrinth) => {
	for (let column in labyrinth) {
		for (let row in labyrinth[column]) {
			if (labyrinth[column][row] == 2)
				return [parseInt(column), parseInt(row)];
		}
	}
	return false;
}

PATHFINDER.get_cross = (labyrinth, center) => {
	let cross = [[1, 1, 1], [1, 1, 1], [1, 1, 1]];
	if (center[0] > 0 && center[0] < labyrinth.length && center[1] >= 0 && center[1] < labyrinth[center[0]].length)
		cross[0][1] = labyrinth[center[0]-1][center[1]]
	if (center[0] >= 0 && center[0] < labyrinth.length-1 && center[1] >= 0 && center[1] < labyrinth[center[0]].length)
		cross[2][1] = labyrinth[center[0]+1][center[1]]
	if (center[0] >= 0 && center[0] < labyrinth.length && center[1] > 0 && center[1] < labyrinth[center[0]].length)
		cross[1][0] = labyrinth[center[0]][center[1]-1]
	if (center[0] >= 0 && center[0] < labyrinth.length && center[1] >= 0 && center[1] < labyrinth[center[0]].length-1)
		cross[1][2] = labyrinth[center[0]][center[1]+1]
	return cross
}

PATHFINDER.get_possibilities = (labyrinth, position) => {
	let directions = [];
	let cases = [];
	let cross = PATHFINDER.get_cross(labyrinth, position);
	for (let column=0; column<3; column++) {
		for (let row=0; row<3; row++) {
			if (cross[column][row] == 0 || cross[column][row] == 3) {
				directions.push([column-1+position[0], row-1+position[1]]);
				cases.push(cross[column][row]);
			}
		}
	}
	return {directions: directions, cases: cases};
}

PATHFINDER.calculate_paths = (labyrinth, paths) => {
	new_paths = [];
	for (let path of paths) {
		let possibilities = PATHFINDER.get_possibilities(labyrinth, path[path.length-1]);
		if (possibilities.cases.includes(3)) {
			new_paths = path.slice();
			new_paths.push(possibilities.directions[possibilities.cases.indexOf(3)]);
			return {paths: new_paths, end: true}
		} else {
			for (let direction of possibilities.directions) {
				if (!PATHFINDER.includes(path, direction)) {
					let free = true;
					for (let path2 of paths) {
						if (PATHFINDER.includes(path2, direction)) {
							free = false;
							break;
						}
					}
					for (let path2 of new_paths) {
						if (PATHFINDER.includes(path2, direction)) {
							free = false;
							break;
						}
					}
					if (free) {
						new_paths.push(path.slice());
						new_paths[new_paths.length-1].push(direction);
					}	
				}
			}
		}
	}
	return {paths: new_paths, end: false};
}

PATHFINDER.resolve = (labyrinth) => {
	paths = [[PATHFINDER.find_start(labyrinth)]];
	end = false;
	while (!end) {
		let result = PATHFINDER.calculate_paths(labyrinth, paths);
		paths = result.paths;
		end = result.end;
		if (paths.length == 0)
			end = true;
	}
	return paths;
}

PATHFINDER.includes = (a, b) => {
	for (let ae=0; ae < a.length; ae++) {
		if (a[ae][0]==b[0] && a[ae][1]==b[1]) {
			return true;
		}
	}
	return false;
}

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
			callback(labyrinth);
		});
		reader.readAsText(file);
	});
}

PATHFINDER.import_conversion = (labyrinth) => {
	labyrinth.replace(labyrinth[2], "2");
	labyrinth.replace(labyrinth[4], "3");
	labyrinth.replace(labyrinth[6], "0");
	labyrinth.replace(labyrinth[8], "1");
	labyrinth = labyrinth.split("\n");
	labyrinth.shift();
	for (let column in labyrinth) {
		labyrinth[column] = Array.from(labyrinth[column]);
		for (let row in labyrinth[column]) {
			labyrinth[column][row] = parseInt(labyrinth[column][row]);
		}
	}
	return labyrinth;
}

PATHFINDER.export_conversion = (labyrinth) => {
	let exported = "[S2E3P0W1]";
	for (let row of labyrinth) {
		exported += "\n";
		for (let element of row) {
			exported += element.toString();
		}
	}
	return exported;
}