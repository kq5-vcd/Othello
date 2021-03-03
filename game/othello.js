let board = [[0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 1, 2, 0, 0, 0],
			 [0, 0, 0, 2, 1, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0]];

let turn = 1;
let block = 0;
let level = 1;

let allowMoves;
let status;
let score;
let levelDown;

const toId = (x, y) => {
	return "tile-" + x + "-" + y;
}

const makeBoard = () => {
	const main = document.getElementById("board");
	while(main.firstChild) {
		main.removeChild(main.firstChild);
	}

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
	//console.log(flippy);

	for(k = 0; k < flippy.length; k++) {
		flipTile(flippy[k][0], flippy[k][1], color);
	}
}

let announce = () => {
	let result = score();
	let game = document.getElementById("player");

	if(result[0] == result[1]) {
		document.getElementById("turn").innerHTML = "Draw";
		return;
	}

	let next = (result[0] < result[1]) ? "blue" : "red";
	let prev = (turn - 1) ? "blue" : "red";

	document.getElementById("turn").innerHTML = "Winner: ";

	game.classList.remove(prev);
	game.classList.add(next);
}

async function makeMove(id, tiles) {
	let avail = await eel.available_tiles(board, turn)();
	let futureFlip = [];

	//console.log(id);
	let color = (turn - 1) ? "blue" : "red";
	let x = id[5];
	let y = id[7];

	for(i = 0; i < avail.length; i++) {
		//console.log(avail[i][0], avail[i][1]);
		if(x == avail[i][0] && y == avail[i][1]) {
			futureFlip = avail[i][2];
			break;
		}
	}

	board[x][y] = turn;
	setPiece(x, y, color);
	flip(futureFlip, color);
	//console.log(board);

	switchPlayer(tiles);
}

async function computerTurn(tiles) {
	let move = await eel.computer_move(board, turn, tiles, level)();
	console.log(move, level);

	let color = (turn - 1) ? "blue" : "red";
	let x = move[0];
	let y = move[1];

	board[x][y] = turn;
	setPiece(x, y, color);
	flip(move[2], color);

	switchPlayer(tiles);
}

async function switchPlayer(moves) {
	for(l = 0; l < moves.length; l++) {
		let revId = toId(moves[l][0], moves[l][1]);
		document.getElementById(revId).onclick = () => {
			return false;
		}
		document.getElementById(revId).classList.remove("available");
	}

	turn = 3 - turn;
	status();
	let avail = await eel.available_tiles(board, turn)();

	if(turn == 1 || avail.length == 0) {
		allowMoves(avail);

		if(level != 1) {
			document.getElementById("neo"). onclick = () => {
				levelDown();
			}
		}
		if(level != 6) {
			document.getElementById("smith").onclick = () => {
				levelUp();
			}
		}
	} else {
		computerTurn(avail);
		document.getElementById("neo"). onclick = () => {
			return false;
		}

		document.getElementById("smith").onclick = () => {
			return false;
		}
	}
}

allowMoves = (moves) => {
	if(moves.length == 0) {
		block++;

		if(block == 2) {
			console.log("End");
			announce();
			return;
		}

		switchPlayer([]);
		return;
	}

	block = 0;

	if(turn == 1) {
		for(i = 0; i < moves.length; i++) {
			let x = moves[i][0];
			let y = moves[i][1];
			let id = toId(x, y);
			//console.log(id);

			document.getElementById(id).classList.add("available");
			document.getElementById(id).onclick = () => {
				makeMove(id, moves);
			} 
		}
	}
}

const initPieces = () => {
	setPiece(3, 3, "red");
	setPiece(4, 4, "red");
	setPiece(3, 4, "blue");
	setPiece(4, 3, "blue");
}

score = () => {
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

status = () => {
	let gameStatus = score();
	let game = document.getElementById("player");
	let next = (turn - 1) ? "blue" : "red";
	let prev = (turn - 1) ? "red" : "blue";

	document.getElementById("red").innerHTML = gameStatus[0];
	document.getElementById("blue").innerHTML = gameStatus[1];

	game.classList.remove(prev);
	game.classList.add(next);
}

const levelUp = () => {
	level++;
	if(level == 6) {
		document.getElementById("smith"). onclick = () => {
			return false;
		}
	}

	document.getElementById('level').innerHTML = "Level " + level;
	document.getElementById("neo").onclick = () => {
		levelDown();
	}

	console.log("Level: " + level);
}

levelDown = () => {
	level--;
	if(level == 1) {
		document.getElementById("neo"). onclick = () => {
			return false;
		}
	}

	document.getElementById('level').innerHTML = "Level " + level;
	document.getElementById("smith").onclick = () => {
		levelUp();
	}

	console.log("Level: " + level);
}

async function newGame() {
	board = [[0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 1, 2, 0, 0, 0],
			 [0, 0, 0, 2, 1, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0]];
	turn = 1;
	block = 0;
	level = 1;

	makeBoard();
	initPieces();
	status();
	document.getElementById("turn").innerHTML = "Turn: ";

	let moves = await eel.available_tiles(board, turn)();
	allowMoves(moves);

	document.getElementById('level').innerHTML = "Level " + level;
	document.getElementById("neo"). onclick = () => {
		return false;
	}

	document.getElementById("smith").onclick = () => {
		levelUp();
	}
}

document.getElementById("reset").onclick = () => {
	newGame();
}

newGame();