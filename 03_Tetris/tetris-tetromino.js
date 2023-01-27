class Tetromino{
    constructor(ctx){
        this.ctx = ctx;
        //this.getNextTetromino();
        const tetrominoNames = ['I', 'J', 'L', 'O', 'S', 'T', 'Z'];
        const rand = Math.floor(Math.random() * tetrominoNames.length); // 랜덤 추출
        this.name = tetrominoNames[rand];  // 블록 모양 저장
        this.array = SHAPES[this.name];  // 블록 배열값 저장
        this.color = COLORS[this.name];
        this.x = 0;           // 게임판 위치는 tmpX, 대기판 위치는 0
        this.y = 0;
        this.setStartPosition();
    }

    setStartPosition(){
        this.x = this.name === 'O' ? COLS / 2 - 1: COLS / 2 - 2;  // 'O' 블록만 좌표 (4,0)에서 시작. 나머지는 (3,0)
        this.y = this.name === 'I' ? -1: 0;   // 'I' 블록만 y좌표 -1에서 시작. 나머지는 0
    }



    draw(){
        this.ctx.fillStyle = this.color;
        this.array.forEach((row, y) => {
            row.forEach((value, x) => {
                if(value){
                    this.ctx.fillRect( (this.x + x) * BLOCK_SIZE, (this.y + y) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);  // 블록 경계선 그리기 위해 1보다 조금 작게 함
                }
            })
        });
    }

    rotate(array) {
        // 블록 회전
        const N = array.length - 1;
        const rotated = array.map((row, i) =>     // i = row index
            row.map((val, j) => array[N - j][i])  // j = col index
        );
        return rotated;
    }


}