class GameBoard{
    constructor(ctx, ctxNext){
        this.ctx = ctx;
        this.ctxNext = ctxNext;
        this.init();
    }

    init(){
        // 보드판 크기 계산
        this.ctx.canvas.width = COLS * BLOCK_SIZE;
        this.ctx.canvas.height = ROWS * BLOCK_SIZE;
        this.ctxNext.canvas.width = 6 * BLOCK_SIZE;
        this.ctxNext.canvas.height = 5 * BLOCK_SIZE;
        // 보드판 그릴 때 사용할 2차원 배열 만들어 0으로 채우기
        this.boardArray = Array.from( {length:ROWS}, () => Array(COLS).fill(0) );
        // 스케일 설정
        //this.ctx.scale(BLOCK_SIZE, BLOCK_SIZE);
        //this.ctxNext.scale(BLOCK_SIZE, BLOCK_SIZE);
    }

    reset(){
        // 게임판 지우기
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        // 게임판 그리기
        gameboard.drawBoard();
    }

    drawBoard(){
        this.boardArray.forEach( (row, y) => {
            row.forEach( (value, x) => {
                if(value){
                    const name = value;   // 게임판의 블록명 가져오기
                    this.ctx.fillStyle = COLORS[name];
                    this.ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
                }
            })
        })
    }

    isValidMove(tetroArray, toMoveX, toMoveY){
        // 이동하려는 곳이 유효한지 확인
        for (let row = 0; row < tetroArray.length; row++) {
            for (let col = 0; col < tetroArray[row].length; col++) {
              if (tetroArray[row][col] && (    // 블록 배열값이 0이 아니면서 그 때의 x, y좌표가
                  col + toMoveX < 0 ||                                // 이동할 곳이 왼쪽 벽을 지나거나
                  col + toMoveX >= COLS ||                            // 이동할 곳이 오른쪽 벽을 지나거나
                  row + toMoveY >= ROWS ||                            //이동할 곳이 게임판 길이 이상이거나
                  this.boardArray[row + toMoveY][col + toMoveX] ))    // 다른 블록에 부딪히면 = 게임판에 블록 문자가 있으면 
              {
                  return false; 
              }
            }
          }
          return true;  // 이동할 곳이 게임판 안쪽이면 true 반환
    }

    getNewTetro(){
        this.next = new Tetromino(this.ctxNext);
        this.ctxNext.clearRect(0, 0, this.ctxNext.canvas.width, this.ctxNext.canvas.height);
        this.next.draw();
    }

    tetroToBoard(tetro) {
        for (let row = 0; row < tetro.array.length; row++) {
            for (let col = 0; col < tetro.array[row].length; col++) {
                if (tetro.array[row][col]) {
                    
                    // 블록이 게임판 위쪽 밖으로 벗어나면 게임 종료
                    if (row + tetro.y < 0) {
                        return showGameOver();
                    }
                    // 블록 위치의 게임판에 블록 이름 입력
                    this.boardArray[row + tetro.y][col + tetro.x] = tetro.name;
                }
            }
        }

        // 채워진 행부터 위쪽으로 모든 셀이 다 채워졌는지 검사
        for (let row = ROWS - 1; row >= 0; ) {
            if (this.boardArray[row].every(cell => cell)) {     //행의 모든 셀이 다 채워졌으면
                // drop every row above this one
                for (let r = row; r > 0; r--) {              // 바로 위의 행으로 바꾸기
                    for (let c = 0; c < COLS; c++) {
                        this.boardArray[r][c] = this.boardArray[r-1][c];
                    }
                }
            }
            else {      
                row--;  // 한 행 위로 올라간다. for문의 세번째 조건을 여기에 쓴다.
            }
        }
    }
}