let dir = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]];
let board = [[0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 1, 2, 0, 0, 0],
			 [0, 0, 0, 2, 1, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0]];

console.log(board);

let availableMoves;
let turn = 1;

const toId = (x, y) => {
	return "tile-" + x + "-" + y;
}

const onBoard = (x, y) => {
	if(x >= 0 && x < 8 && y >= 0 && y < 8) {
		return 1;
	}
	return 0;
}

const tilesToFlip = (x, y, xDir, yDir) => {
	let flippedTiles = [];
	let other = 3 - turn;
	let moveX = x;
	let moveY = y;

	moveX += xDir;
	moveY += yDir;

	if(onBoard(moveX, moveY) == 0) {
		return [];
	}

	while(board[moveX][moveY] == other) {
		flippedTiles.push([moveX, moveY]);
		moveX += xDir;
		moveY += yDir;

		if(!onBoard(moveX, moveY)) {
			return [];
		}
	}

	if(board[moveX][moveY] == turn) {
		return [];
	}

	if(flippedTiles.length > 0) {
		if(board[moveX][moveY] == 0) {
			return [moveX, moveY, flippedTiles];
		}
	}

	return [];
}

const tilesForOne = (x, y) => {
	let validTiles = [];

	for(a = 0; a < dir.length; a++) {
		let xM = dir[a][0];
		let yM = dir[a][1];
		let tiles = tilesToFlip(x, y, xM, yM);

		if(tiles.length > 0) {
			validTiles.push(tiles);
		}
	}
	console.log(validTiles);

	return validTiles;
}

const validTiles = () => {
	let validTiles = [];
	for(i = 0; i < 8; i++) {
		for(j = 0; j < 8; j++) {
			//console.log(i, j);
			if(board[i][j] == turn) {
				//console.log(i, j);
				let oneTiles = tilesForOne(i, j);

				for(k = 0; k < oneTiles.length; k++) {
					validTiles.push(oneTiles[k]);
				}
				//console.log(i, j);
			}
		}
	}
	return validTiles;
}

const makeBoard = () => {
	for(i = 0; i < 8; i++) {
		let row = document.createElement("div");
		row.className = "tab-row";

		for(j = 0; j < 8; j++) {
			let tile = document.createElement("div");
			tile.className = "tile";
			tile.id = toId(i , j);

			row.appendChild(tile);
		}

		document.getElementById("board").appendChild(row);
	}	
}

const setPiece = (x , y, color) => {
	let id = toId(x, y);
	let piece = document.createElement("div");
	
	piece.className = "piece";
	piece.classList.add(color);

	document.getElementById(id).appendChild(piece);
} 

const initPieces = () => {
	setPiece(3, 3, "red");
	setPiece(4, 4, "red");
	setPiece(3, 4, "blue");
	setPiece(4, 3, "blue");
}

const flipTile = (x, y, color) => {
	let id = toId(x, y);
	let piece =document.getElementById(id).firstChild;
	let other = (color == "red") ? "blue" : "red";

	piece.classList.remove(other);
	piece.classList.add(color);

	board[x][y] = 3 - board[x][y];
}

const flip = (tileArr, color) => {
	let flippy = tileArr;
	console.log(flippy);

	for(k = 0; k < flippy.length; k++) {
		flipTile(flippy[k][0], flippy[k][1], color);
	}
}

const switchPlayer = (tileArr) => {
	turn = 3 - turn;
	let remove = tileArr;

	for(l = 0; l < remove.length; l++) {
		let revId = toId(remove[l][0], remove[l][1]);
		document.getElementById(revId).onclick = () => {
			return false;
		}
		document.getElementById(revId).classList.remove("available");
	}

	availableMoves();
	status();
}

const makeMove = (id) => {
	let avail = validTiles();
	let futureFlip = [];

	console.log(id);
	let color = (turn - 1) ? "blue" : "red";
	let x = id[5];
	let y = id[7];

	for(i = 0; i < avail.length; i++) {
		console.log(avail[i][0], avail[i][1]);
		if(x == avail[i][0] && y == avail[i][1]) {
			for(j = 0; j < avail[i][2].length; j++) {
				futureFlip.push(avail[i][2][j]);
			}
		}
	}

	board[x][y] = turn;
	setPiece(x, y, color);
	flip(futureFlip, color);
	console.log(board);

	switchPlayer(avail);
}

availableMoves = () => {
	let available = validTiles();
	console.log(available);

	if(available.length == 0) {
		switchPlayer([]);
	}

	for(i = 0; i < available.length; i++) {
		let x = available[i][0];
		let y = available[i][1];
		let id = toId(x, y);
		console.log(id);

		document.getElementById(id).classList.add("available");
		document.getElementById(id).onclick = () => {
			makeMove(id);
		} 
	}
}

const score = () => {
	let scores = [0 , 0];

	for(a = 0; a < 8; a++) {
		for(b = 0; b < 8; b++) {
			if(board[a][b] != 0) {
				scores[board[a][b] - 1]++;
			}
		}
	}

	return scores;
}

const status = () => {
	let gameStatus = score();
	let game = document.getElementById("player");0
	let next = (turn - 1) ? "blue" : "red";
	let prev = (turn - 1) ? "red" : "blue";

	document.getElementById("red").innerHTML = gameStatus[0];
	document.getElementById("blue").innerHTML = gameStatus[1];

	game.classList.remove(prev);
	game.classList.add(next);
}

makeBoard();
initPieces();
availableMoves();
status();