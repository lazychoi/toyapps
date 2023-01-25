const ctx = document.getElementById('game').getContext('2d');
const grid = 32;            // 320px/10열 = 32, 640px/20행 = 32 => 한 셀의 크기 32x32
const tetrominoSequence = [];

/**
 * how to draw each tetromino
 * @see https://tetris.fandom.com/wiki/SRS
 * keep track of what is in every cell of the game using a 2d array 
 * 게임판의 모든 셀에 무엇이 있는지 추적
 * tetris playfield is 10x20, with a few rows offscreen
 */ 
const playfield = [];
// populate the empty state
for (let row = -2; row < 20; row++) {       // 22 행???  
    playfield[row] = [];

    for (let col = 0; col < 10; col++) {
        playfield[row][col] = 0;
    }
}

const tetrominos = {
    'I': [
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0]
    ],
    'J': [
        [1,0,0],
        [1,1,1],
        [0,0,0],
    ],
    'L': [
        [0,0,1],
        [1,1,1],
        [0,0,0],
    ],
    'O': [
        [1,1],
        [1,1],
    ],
    'S': [
        [0,1,1],
        [1,1,0],
        [0,0,0],
    ],
    'Z': [
        [1,1,0],
        [0,1,1],
        [0,0,0],
    ],
    'T': [
        [0,1,0],
        [1,1,1],
        [0,0,0],
    ]
};

// color of each tetromino
const colors = {
    'I': 'cyan',
    'O': 'yellow',
    'T': 'purple',
    'S': 'green',
    'Z': 'red',
    'J': 'blue',
    'L': 'orange'
};

let count = 0;
let tetromino = getNextTetromino();
let rAF = null;  // keep track of the animation frame so we can cancel it 애니메이션을 취소할 수 있도록 추적하는 변수
let gameOver = false;

// min, max 범위 내에서 랜덤 정수 추출
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
  
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  // 블록 순서 정하기
  function generateSequence() {
    const sequence = ['I', 'J', 'L', 'O', 'S', 'T', 'Z'];
  
    while (sequence.length) {
      const rand = getRandomInt(0, sequence.length - 1);
      const name = sequence.splice(rand, 1)[0];       // splice는 배열 반환
      tetrominoSequence.push(name);
    }
  }
  
  // 다음 순서 블록 가져오기
  function getNextTetromino() {
    if (tetrominoSequence.length === 0) {   // 블록 랜덤하게 섞어 순서 만들기
      generateSequence();
    }
  
    const name = tetrominoSequence.pop();
    const matrix = tetrominos[name];  // 블록 배열값 저장
  
    // I, O는 중앙에서, 나머지는 왼쪽 중앙에서 시작
    const col = playfield[0].length / 2 - Math.ceil(matrix[0].length / 2);
  
    // I 시작위치 -> row 21(-1), 나머지 -> row 22(-2) I는 4x4이기 때문에
    const row = name === 'I' ? -1 : -2;
  
    return {
      name: name,      // name of the piece (L, O, etc.)
      matrix: matrix,  // the current rotation matrix
      row: row,        // current row (starts offscreen)
      col: col         // current col
    };
  }
  
  // rotate an NxN matrix 90deg
  // @see https://codereview.stackexchange.com/a/186834
  function rotate(matrix) {
    const N = matrix.length - 1;
    const result = matrix.map((row, i) =>
      row.map((val, j) => matrix[N - j][i])
    );
    return result;
  }
  
  // 이동하려는 matrix/row/col이 유효한지 확인
  function isValidMove(matrix, cellRow, cellCol) {
    for (let row = 0; row < matrix.length; row++) {
      for (let col = 0; col < matrix[row].length; col++) {
        if (matrix[row][col] && (
            // outside the game bounds
            cellCol + col < 0 ||                  // cellcol : 이동하려는 x 좌표
            cellCol + col >= playfield[0].length ||
            cellRow + row >= playfield.length ||
            // collides with another piece
            playfield[cellRow + row][cellCol + col])
          ) {
          return false;
        }
      }
    }
  
    return true;
  }
  
  // place the tetromino on the playfield   비활성 블록을 게임판으로 변환
  function placeTetromino() {
    for (let row = 0; row < tetromino.matrix.length; row++) {
      for (let col = 0; col < tetromino.matrix[row].length; col++) {
        if (tetromino.matrix[row][col]) {
  
          // 블록이 게임판 위쪽 밖으로 벗어나면 게임 종료
          if (tetromino.row + row < 0) {
            return showGameOver();
          }
          playfield[tetromino.row + row][tetromino.col + col] = tetromino.name;
        }
      }
    }
  
    // check for line clears starting from the bottom and working our way up 게임판 맨 아래행부터 모든 셀이 다 채워졌는지 검사
    for (let row = playfield.length - 1; row >= 0; ) {
      if (playfield[row].every(cell => !!cell)) {     //행의 모든 셀이 다 채워졌으면?? cell => cell 이게 뭐지??
  
        // drop every row above this one
        for (let r = row; r >= 0; r--) {              // 바로 위의 행으로 바꾸기
          for (let c = 0; c < playfield[r].length; c++) {
            playfield[r][c] = playfield[r-1][c];
          }
        }
      }
      else {
        row--;
      }
    }
  
    tetromino = getNextTetromino();
  }
  
  // show the game over screen
  function showGameOver() {
    cancelAnimationFrame(rAF);
    gameOver = true;
  
    ctx.fillStyle = 'black';
    ctx.globalAlpha = 0.75;       // 투명도
    ctx.fillRect(0, ctx.canvas.height / 2 - 30, ctx.canvas.width, 60);       // GAME OVER 글자 배경색
  
    ctx.globalAlpha = 1;
    ctx.fillStyle = 'white';
    ctx.font = '36px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('GAME OVER!', ctx.canvas.width / 2, ctx.canvas.height / 2);
  }
  
  // game loop
  function loop() {
    rAF = requestAnimationFrame(loop);
    ctx.clearRect(0,0,ctx.canvas.width, ctx.canvas.height);    // 320 x 640 <- html에서 설정함
      
    // draw the playfield
    for (let row = 0; row < 20; row++) {
      for (let col = 0; col < 10; col++) {
        if (playfield[row][col]) {
          const name = playfield[row][col];  // 게임판의 블록 위치에 블록 이름 부여
          // console.log('게임판의 블록', name)
          ctx.fillStyle = colors[name];
  
          // drawing 1 px smaller than the grid creates a grid effect 한 셀의 크기=grid -> col(x), row(y) * grid -> 시작좌표 // -1은 테두리가 생기도록 하기 위해
          ctx.fillRect(col * grid, row * grid, grid-1, grid-1);
        }
      }
    }
  
    // draw the active tetromino
    if (tetromino) {
  
      // tetromino falls every 35 frames 35 <- 세로 32셀 + 블록자체셀 3 ???
      if (++count > 35) {     // 떨어지는 속도 조절
        tetromino.row++;
        count = 0;
  
        // place piece if it runs into anything   이동하려는 위치가 유효하지 않으면 멈춤
        if (!isValidMove(tetromino.matrix, tetromino.row, tetromino.col)) {
          tetromino.row--;
          placeTetromino();
        }
      }
  
      ctx.fillStyle = colors[tetromino.name];
  
      for (let row = 0; row < tetromino.matrix.length; row++) {
        for (let col = 0; col < tetromino.matrix[row].length; col++) {
          if (tetromino.matrix[row][col]) {
  
            // drawing 1 px smaller than the grid creates a grid effect // tetromino.col: 초기 블록 모양에서 왼쪽벽으로 가면 0, 오른쪽벽은 7. 회전하면 값이 바뀜
            ctx.fillRect((tetromino.col + col) * grid, (tetromino.row + row) * grid, grid-1, grid-1); 
              // console.log(tetromino.col)
          }
        }
      }
    }
  }
  
  // listen to keyboard events to move the active tetromino active 블록을 움직이기 위해 키 입력 처리
  document.addEventListener('keydown', function(e) {
    if (gameOver) return;
  
    // left and right arrow keys (move)
    if (e.key == 'ArrowLeft' || e.key == 'ArrowRight') {
      const col = e.key === 'ArrowLeft'
        ? tetromino.col - 1
        : tetromino.col + 1;
  
      if (isValidMove(tetromino.matrix, tetromino.row, col)) {
        tetromino.col = col;
      }
    }
  
    // up arrow key (rotate)
    if (e.key == 'ArrowUp') {
      const matrix = rotate(tetromino.matrix);
      if (isValidMove(matrix, tetromino.row, tetromino.col)) {
        tetromino.matrix = matrix;
      }
    }
  
    // down arrow key (drop)
    if(e.key = 'ArrowDown') {
      const row = tetromino.row + 1;
  
      if (!isValidMove(tetromino.matrix, row, tetromino.col)) {
        tetromino.row = row - 1;      // 아래쪽으로 한 칸 이동한 값을 되돌리기
  
        placeTetromino();
        return;
      }
  
      tetromino.row = row;
    }
  });
  
  // start the game
  rAF = requestAnimationFrame(loop);