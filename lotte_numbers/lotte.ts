let lotte: number[] = new Array(7);
const numPool: number[] = new Array(45);
for(let i=1; i<46; i++)      // 뽑을 숫자 
{
    numPool[i] = i;
    // console.log(numPool[i]);
}

function choose(): number
{    
    let num: number = Math.floor(Math.random() * 45) + 1; // 특정 범위에서 난수 뽑기 => Math.random() * (max - min + 1) + min
    numPool.splice(num-1, 1);                             // 배열.splice(index, 삭제할 개수) 인덱스는 0부터 시작 -> 난수는 1부터
    return num;
}

for(let i=0; i<7; i++){
    let tmp = choose();
    lotte[i] = tmp;
    // console.log("numPool 남은 숫자 개수", numPool.length);
}

let result: string = '';
for(let i=0; i<7; i++)
    result += lotte[i] + " ";

console.log("로또 번호는", result);

/**
 * 알고리즘
 * 1. 변수
 * 1.1. lotte[7] : 로또 번호 담은 최종 반환값
 * 1.2. numPool: 1-45 숫자 모음(중복 번호 제외 위해 필요)
 * 1.3. tmp: 랜덤하게 뽑은 숫자 저장
 * 2. choose() 메서드
 * 2.1. numPool에서 랜덤하게 숫자 1개 뽑아 반환
 * 2.2. 뽑은 숫자를 numPool에서 제거
 * 3. 메인
 * 3.1. for문 7번 반복
 * 3.2. tmp <- choose() 메서드 호출하여 반환값
 * 3.3. lotte <- tmp 
 * 
 * ===> 개선 : 로또 번호 맞추기 게임
 */
