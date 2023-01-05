(function() {
"use strict"

let lotte = [];

// 뽑기 pool에 담길 숫자
const items = [];
for(let i=1; i<46; i++)
items.push(i);

// 하단에 추첨 기호 표시
// document.querySelector(".info").textContent = items.join(' ');

const doors = document.querySelectorAll(".door");              // 각 숫자 
document.querySelector("#spinner").addEventListener("click", spin);
document.querySelector("#reseter").addEventListener("click", init);

async function spin() {
    lotte = [];
    init(false, 1, 2);                               // 초기화(false=아무 일도 안 함, groups=1, duration=애니메이션1초)
    for ( const door of doors){                                // 숫자 안의
        const boxes = door.querySelector(".boxes");                      // boxes 클래스 선택하여
        const duration = parseInt(boxes.style.transitionDuration);      // 지정된 애니메이션 시간 가져와
        boxes.style.transform = "translateY(0)";                        // boxes를 세로 위끝으로 설정 -> 최종 위치???
        await new Promise((resolve) => setTimeout(resolve, duration * 100));  // ??? 0.1초씩 지연시킴
    }
    console.log(lotte)
    // 로또 번호 중복 검사
    for(let i=0; i<lotte.length-1; i++){
        for(let j=i+1; j<lotte.length; j++){
            if ( lotte[i] == lotte[j]) { 
                console.log("중복 숫자 존재"); 
                break;
            }
        }
    }

}

function init(firstInit = true, groups = 1, duration = 1) {
    for (const door of doors) {         // 각 숫자를 돌며
        if (firstInit) {                        // firstInit -> 참이면
            door.dataset.spinned = "0";          // data-spinned -> 0 으로 설정(초기화???)
        } else if (door.dataset.spinned === "1") {  // data-spinned -> 1이면(추첨이 끝났으면)
            return;                             // 아무 것도 안 함
        }

        const boxes = door.querySelector(".boxes");  // boxes를
        const boxesClone = boxes.cloneNode(false);  // 복제. 왜???? 해당 node의 children 까지 복제하려면 true, 해당 node 만 복제하려면 false

        const pool = ["?"];      // 시작 시 화면에 나타나는 값
        if (!firstInit) {        // firstInit -> false이면 
            const arr = [];
            // for (let n = 0; n < (groups > 0 ? groups : 1); n++)  // group 개수만큼 순회 -> group은 없어도 되는데... 무슨 용도로 넣은 걸까?
            // {
                arr.push(...items);                            // arr 배열에 로또 전체 숫자 넣기
            // }
            pool.push(...shuffle(arr));                        // 순서 뒤섞어 pool에 넣기 -> 각 pool의 마지막 숫자가 최종 번호

            // console.log("pool", pool[pool.length-1])
            let isSame = true;
            while(isSame)         // 당첨번호배열에 같은 숫자가 있으면 다시 돌리기
            {           
                if(!lotte.includes(pool[pool.length-1])) { isSame = false; break;}
                pool.push(...shuffle(arr));
            } 
            lotte.push(pool[pool.length-1]);                   // 당첨번호배열에 당첨번호 넣기

            boxesClone.addEventListener("transitionstart", 
                function ()                                         // 복제한 박스들이 애니메이션을 시작하면
                {
                    door.dataset.spinned = "1";                       // door 태그 data-spinned -> 1로 변경
                    // console.log("this", this);
                    this.querySelectorAll(".box").forEach((box) =>   // 각 숫자 흐림효과
                    {
                        box.style.filter = "blur(1px)";     
                    });
                },
                { once: true }    // event listener가 최대 한 번만 동작. true -> 수신기가 발동한 후에 스스로를 대상에서 제거. 기본 값은 false
            );

            boxesClone.addEventListener("transitionend",       // 복제한 박스들의 애니메이션이 끝나면
                function () 
                {
                    this.querySelectorAll(".box").forEach((box, index) =>  
                    {
                        box.style.filter = "blur(0)";
                        if (index > 0) this.removeChild(box);     // ???
                    });
                },
                { once: true }
            );
        }

        for (let i = pool.length - 1; i >= 0; i--)             // 모든 숫자를 거꾸로 순회하며
        {
            const box = document.createElement("div");      // 새 노드 생성
            box.classList.add("box");                       // box 클래스 추가
            box.style.width = door.clientWidth + "px";      // 인라인 요소나 CSS 상에 존재하지 않는 요소 -> 0, 그렇지 않다면 엘리먼트의 내부 너비를 픽셀로 나타냄. 내부 너비는 안쪽 여백(패딩)을 포함. 테두리, 바깥 여백(마진), 수직 스크롤바의 너비는 포함하지 않음
            box.style.height = door.clientHeight + "px";
            box.textContent = pool[i];
            boxesClone.appendChild(box);                    // 복제한 요소 자식으로 추가
        }
        boxesClone.style.transitionDuration = `${duration > 0 ? duration : 1}s`;   // 지속시간 -> 최소 1초
        boxesClone.style.transform = `translateY(-${door.clientHeight * (pool.length - 1)}px)`;  // 세로 위치 -> -( door 세로 길이 * door 개수 )px
        door.replaceChild(boxesClone, boxes);               // parentNode.replaceChild(newChild, oldChild)
    }
}

function shuffle([...arr])  // 숫자 뒤섞기 
{
    let m = arr.length;
    while (m) 
    {
        const i = Math.floor(Math.random() * m--);   // m 인덱스의 값 <-> 0~m 중 랜덤 숫자 인덱스의 값
        [arr[m], arr[i]] = [arr[i], arr[m]];
    }
    return arr;
}
init();
})();

