
class NextBoard{
    constructor(ctxNext){
        this.ctx = ctxNext;
        this.init();
    }

    init(){
        this.width = 6 * BLOCK_SIZE;
        this.height = 5 * BLOCK_SIZE;
        ctx.scale(BLOCK_SIZE, BLOCK_SIZE);
    }

    reset(){
        this.nextboardArray = Array.from( {length:5}, () => Array(6).fill(0) );
        this.ctx.clearRect(0, 0, this.width, this.height);    // next 캔버스 지우기
        this.next = new Tetromino(this.ctx);
        console.log(this.next);
        this.next.x = 1;
        this.next.y = 1;
        this.next.draw();                               // 다음 블록 그리기
    }

    drawBoard(){
        this.nextboardArray.forEach( (row, y) => {
            row.forEach( (value, x) => {
                if(value > 0){
                    this.ctx.fillStyle = COLORS[this.tetro.name];
                    this.ctx.fillRect(x, y, 0.96, 0.96);
                }
            })
        })
    }

}

