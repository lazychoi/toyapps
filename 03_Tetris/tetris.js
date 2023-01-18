'use strict';

/**
 * 기본 설정값 변수에 할당
 * 1. 게임 보드 행, 열, 셀 크기
 * 2. 색상
 * 3. 블록 모양
 * 4. 키보드 입력값
 */

// 게임 보드 크기 설정
const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30;

const COLORS = [ 'none', 'cyan', 'blue', 'orange', 'yellow', 'green', 'purple', 'red' ];
const SHAPES = [
    [],                 // WHY?? 빈 것은 왜 필요할까?
    [[0, 0, 0, 0],      // I
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[2, 0, 0],         // J
     [2, 2, 2],
     [0, 0, 0]],
    [[0, 0, 3],         // L
     [3, 3, 3],
     [0, 0, 0]],
    [[4, 4],            // ㅁ
     [4, 4]],
    [[0, 5, 5],         // S
     [5, 5, 0],
     [0, 0, 0]],
    [[0, 6, 0],         // ㅗ
     [6, 6, 6],
     [0, 0, 0]],
    [[7, 7, 0],         // ㄹ
     [0, 7, 7],
     [0, 0, 0]]
];

const KEY = {   // 키보드 Enum 
    ESC: 27,
    SPACE: 32,
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40,
    P: 80,
    Q: 81
};

const ROTATION = {
    LEFT: 'left',
    RIGHT: 'right'
};

[COLORS, SHAPES, KEY, ROTATION].forEach(item => Object.freeze(item)); //변경 불가능하게 설정


/**
 * 보드 클래스
 * 1. 생성자 메서드: 2개의 2d context를 매개변수로 받음(메인보드, next 보드)
 * 2. 보드판 크기 설정 <- init()
 * 3. 초기화 메서드 <- reset()
 * 3.1. 보드판 비우기 메서드 = 값을 0으로 할당 <- getEmptyGrid()
 * 3.2. 블록 객체 생성
 * 3.3. 블록이 처음 놓일 위치 설정 <- 블록 클래스 setStartingPosition()
 * 3.4. NextCanvas에서 블록 객체 가져오기 <- getNewPiece() 
 * 3.5. NextCanvas 블록 지우기 <- clearRect()
 * 3.6. 보드판에 블록 그리기  -> 블록 클래스 draw() 메서드
 * 3.7. 보드판 그리기 <- 블록 클래스 draw(), draw()
 * 4. 블록 회전 <- rotate()
 * 4.1. 
 *  */ 
// 빈 셀 = 0, 색상=[1-7]
class Board {

    constructor(cts, ctxNext){
        this.ctx = ctx;
        this.ctxNext = ctxNext;
        this.init()
    }

    // 보드판 크기 설정
    init(){
        this.ctx.canvas.width = COLS * BLOCK_SIZE;   // 10*30=300px
        this.ctx.canvas.height = ROWS * BLOCK_SIZE;  // 20*30=600px
        this.ctx.scale(BLOCK_SIZE, BLOCK_SIZE);      // 그리는 기본 셀 크기를 30px로 설정
    }
    // Reset the Board when starting a new game
    reset() {
        this.grid = this.getEmptyGrid();     // 각 셀을 0으로 채움
        this.piece = new Piece(this.ctx);    // 블록 객체 생성
        this.piece.setStartingPosition();    // 블록이 처음에 놓일 보드의 x축 좌표 ㅁ-> 4, 나머지 -> 3
        this.getNewPiece();
    }

    getEmptyGrid() {     // 각 셀을 0으로 채움
        return Array.from (      // Array.from(arrayLike, mappingFuction)
            {length: ROWS}, () => Array(COLS).fill(0)
        );
    }

    getNewPiece() {
        const { width, height } = this.ctxNext.canvas;  // next canvas 크기 가져오기
        this.next = new Piece(this.ctxNext);            // next 블록 객체 생성
        this.ctxNext.clearRect(0, 0, width, height);    // next canvas 지우기
        this.next.draw();       // next 보드에 있던 블록을 보드에 그리기
    }

    draw(){
        this.piece.draw();  // piece 메서드
        this.drawBoard();
    }

    drawBoard(){
        this.grid.forEach( (row, y) => {
            row.forEach( (value, y) => {
                if (value > 0) {
                    this.ctx.fillStyle = COLORS[value];  // value에 해당하는 색상 선택
                    this.ctx.fillRect(x, y, 1, 1);       // 사각형 그리기. scale에 지정한 블록 크기만큼
                }
            });
        });
    }

    rotate(piece, direction) {
        // clone with JSON for immutability ????
        let p = JSON.parse(JSON.stringify(piece));

        // transpose matrix
        for (let y=0; y<p.shape.length; ++y){
            [p.shape[x][y], p.shape[y][x]] = [p.shape[y][x], p.shape[x][y]];
        }

        // reverse the order of the column ????
        if (direction === ROTATION.RIGHT){
            p.shape.forEach( (row) => row.reverse());
        } else if (direction = ROTATION.LEFT) {
            p.shape.reverse();
        }

        return p;
    }
}


/**
 * 블록 클래스
 * 1. 생성자
 * 2. 블록 무작위 생성 <- randomizeTetrominoType()
 * 2.1. 색상 번호 무작위 선택
 * 2.2. 색상 번호로 블록 모양 결정
 * 2.3. x, y 위치 0으로 초기화
 * 3. 블록 보드에 그리기 <- draw()
 * 4. 블록 이동 <- move()
 * 5. 시작 위치 설정 <- setStartingPosition()
 */
class Piece {
    constructor(ctx){
        this.ctx = ctx;
        this.spawn();
    }

    spawn() {
        this.typeID = this.randomizeTetrominoType(COLORS.length); // 원 코드에서는 COLORS.length - 1
        this.shape = SHAPES[this.typeID];
        this.color = COLORS[this.typeID];
        this.x = 0;
        this.y = 0;
    }

    draw(){
        this.ctx.fillStyle = this.color;   // 색상 설정
        this.shape.forEach((row, y) => {   // 블록의 행값과 y 위치를 매개변수로 받는다
            row.forEach( (value, x) => {   // 블록의 값과 x 위치를 매개변수로 받는다
                //this.x, this.y -> 도형의 좌상단 위치
                // x, y -> 도형이 놓일 위치
                // this.x + x -> 보드에서 블록의 위치
                if (value > 0) {      // value가 0보다 큰 곳만 색상을 칠함
                    this.ctx.fillRect( this.x + x, this.y + y, 1, 1 );   // fillRect(x, y, width, height)
                }
            });
        });
    }

    randomizeTetrominoType(noOfTypes){
        return Math.floor(Math.random() * noOfTypes) // 원 코드 noOfTypes + 1
    }

    setStartingPosition() {    // 사각형만 x 좌표 4, 나머지는 3
        this.x = this.tyhpeId === 4 ? 4 : 3;
    }

    move(p) {
        this.x = p.x;
        this.y = p.y;
        this.shape = p.shape;
    }
}

/**
 * 메인 게임
 * 1. DOM 가져오기: 메인보드, next보드 -> 2d context 
 * 2. 게임 점수 초기화
 * 3. 블록을 키보드로 움직이는 객체 <- moves : Computed Property Name을 사용하면 key에 변수를 넣을 수 있다. 요렇게 [변수]
 * 4. 보드 객체 생성 -> 메인보드, next 보드
 * 5. next 보드 크기 설정 <- initNext()
 * 
 */

const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
const canvasNext = document.getElementById('next');
const ctxNext = canvas.getContext('2d');

const moves = {         //  computed property keys
    [KEY.LEFT]: (p) => ( { ...p, x: p.x - 1 } ),
    [KEY.RIGHT]: (p) => ( { ...p, x: p.x + 1 } ),
    [KEY.DOWN]: (p) => ( { ...p, x: p.y + 1 } ),
    [KEY.SPACE]: (p) => ( { ...p, x: p.y + 1 } ),
    [KEY.UP]: (p) => board.rotate(p, ROTATION.RIGHT),
    [KEY.Q]: (p) => board.rotate(p, ROTATION.LEFT)
}

// next 캔버스 크기 설정
ctxNext.canvas.width = 4 * BLOCK_SIZE;
ctxNext.canvas.height = 4 * BLOCK_SIZE;
ctxNext.scale(BLOCK_SIZE, BLOCK_SIZE);

// function addEventListener() {
//     document.removeEventListener('keydown', handleKeyPress);  // 기존 블록을 지우기 위해선가???
//     document.addEventListener('keydown', handleKeyPress);
// }
let board = new Board();

function handleKeyPress(e) {
    let p = moves[e.keyCode](board.piece);
    if (board.valid(p)){
        board.piece.move(p);
    }
}

function play(){
    // addEventListener();
    document.removeEventListener('keydown', handleKeyPress);  // 기존 블록을 지우기 위해선가???
    document.addEventListener('keydown', handleKeyPress);

    board.reset();
    animate();
    
}

function animate(){
    // clear board before drawing new state
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    board.draw();   // 보드 그리기
    requestAnimationFrame(animate);
}

