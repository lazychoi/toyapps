// 1-45번까지 랜덤하게 뽑고 lotte 변수에 넣을 때 중복 여부 검사

let lotte: number[] = new Array();
// let size: number = 0; // lotte 변수에 중복 없는 숫자 개수 체크

function choose(): number
{    
    let num: number = Math.floor(Math.random() * 45) + 1; // 특정 범위에서 난수 뽑기 => Math.random() * (max - min + 1) + min
    return num;
}

while(lotte.length < 7)
{
    let tmp = choose();
    if ( !lotte.includes(tmp) ) // 당첨번호 배열에 같은 숫자가 없으면
        lotte.push(tmp)
}

let result: string = '';
for(let i=0; i<7; i++)
    result += lotte[i] + " ";

console.log("로또 번호는", result);

