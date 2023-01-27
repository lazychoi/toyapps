const canvas = document.getElementById('game-board')
const ctx = canvas.getContext('2d');
const canvasNext = document.getElementById('next')
const ctxNext = canvasNext.getContext('2d');
const btnPlay = document.getElementById('btn-play');
const btnPause = document.getElementById('btn-pause');

let latency = 0; // 블록 떨어지는 속도 조절 변수
let rAF = null;  // keep track of the animation frame so we can cancel it 애니메이션을 취소할 수 있도록 추적하는 변수
let gameOver = false;

let gameboard = new GameBoard(ctx, ctxNext);
let tetro = new Tetromino(ctx);    // 게임판에 넣을 블록 만들기
tetro.setStartPosition();

function loop() {
    // 애니메이션 시작
    rAF = requestAnimationFrame(loop);  // 이곳에 있어야 행이 채워졌을 때 사라짐
    
    // 게임판 새로 그리기
    gameboard.reset();

    // 게임판에 블록 그리기

    if(tetro){
        // 떨어지는 속도 조절. 10번은 같은 위치에서 블록 그림. 11번째 세로로 한 칸 이동
        latency++;
        if(latency > 30) { 
            tetro.y++; 
            latency = 0;
        }
        // 이동할 수 없는 곳인지 점검
        if(!gameboard.isValidMove(tetro.array, tetro.x, tetro.y)){
            tetro.y--;                      // 이동할 수 없는 곳이면 증가한 값 취소
            gameboard.tetroToBoard(tetro);
            tetro = new Tetromino(ctx);
        }
        // 이동할 수 있는 곳이면 블록 그리기
        tetro.draw();
    }
}

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

function play(){
    rAF = requestAnimationFrame(loop);
    btnPlay.style.display = 'none';
    btnPause.style.display = 'block';
}

function pause(){
    cancelAnimationFrame(rAF);
    btnPlay.style.display = 'block';
    btnPause.style.display = 'none';
}

// 키보드 설정
document.addEventListener('keydown', function(e) {

    if (gameOver) return;
    
    // left and right arrow keys (move)
    if (e.key == 'ArrowLeft' || e.key == 'ArrowRight') {
        const moveX = e.key === 'ArrowLeft' ? tetro.x - 1 : tetro.x + 1;
        if (gameboard.isValidMove(tetro.array, moveX, tetro.y)) {
        tetro.x = moveX;
        }
    }
    
    // down arrow key (drop)
    if(e.key = 'ArrowDown') {
        const moveY = tetro.y + 1;
        if (!gameboard.isValidMove(tetro.array, tetro.x, moveY)) {
            tetro.y = moveY - 1;      // 유효한 이동위치가 아니면 증가시킨 y값 되돌리기
            //tetrominoToGamefield();
            return;
        } else {
            tetro.y = moveY;
        }
    }

    // up arrow key (rotate)
    if (e.key == 'ArrowUp') {
        const matrix = tetro.rotate(tetro.array);
        if (gameboard.isValidMove(matrix, tetro.x, tetro.y)) {
            tetro.array = matrix;
        }
    }

    if (e.key == 'p' || e.key == 'P'){
        play();
    }

    if (e.key == 'q' || e.key == 'Q'){
        pause();
    }
});

btnPlay.addEventListener('click', () => {
    play();
})

btnPause.addEventListener('click', () => {
    pause();
})