(function() {
    "use strict"
    
    let lotte = [];        // 당첨 번호
    let bonusNum = 0;      // 보너스 번호
    let selectNum = [];    // 사용자가 선택한 숫자

    // 뽑기 pool에 담길 숫자
    const items = [];
    for(let i=1; i<46; i++)
    items.push(i);
    
    // user-input buttons만들기
    const userNum = document.querySelector(".user-num");
    for(let i=0; i<items.length; i++)
    {
        const input = document.createElement("input");
        input.setAttribute("type", "button");
        input.setAttribute("value", i+1);
        input.classList.add("num");
        userNum.appendChild(input);
    }

    // 로또 번호 생성
    let pools = [];      // 슬롯머신 숫자묶음 7개 생성
    let cnt = 0;
    for(let i=0; i<8; i++)
    {
        let pool = ["?"];      // 시작 시 화면에 나타나는 값
        const arr = [];
        arr.push(...items);           // arr 배열에 로또 전체 숫자 넣기
        pool.push(...shuffle(arr));   // 순서 뒤섞어 pool에 넣기 -> 각 pool의 마지막 숫자가 최종 번호

        let isSame = true;
        while(isSame)         // 당첨번호배열에 같은 숫자가 있으면 다시 돌리기
        {           
            if(!lotte.includes(pool[pool.length-1])) { isSame = false; break;}
            pool = ["?"];                   // 기존 pool을 초기화
            pool.push(...shuffle(arr));
        } 
        lotte.push(pool[pool.length-1]);                   // 당첨번호배열에 당첨번호 넣기
        
        pools.push(pool); 
    }

    // 최종 로또 번호 중복 검사
    for(let i=0; i<lotte.length-1; i++){
        for(let j=i+1; j<lotte.length; j++){
            if ( lotte[i] == lotte[j]) { 
                console.log("중복 숫자 존재"); 
                break;
            }
        }
    }
    // 로또번호 마지막 -> 보너스 번호
    bonusNum = lotte.splice(6, 1)
    console.log("로또번호:", lotte, "\n보너스 번호: ", bonusNum)

    // 사용자 번호 선택
    const nums = document.querySelectorAll(".num");  // 선택 번호(1-45)
    for(let i=0; i<nums.length; i++)
    {
        nums[i].addEventListener("click", () =>
        {
            // nums[i].classList.toggle("selected");
            if(nums[i].className == "num")
            {
                nums[i].classList.add("selected");
                selectNum.push(parseInt(nums[i].value));
                console.log(selectNum);
            } else if (nums[i].className == "num selected")
            {
                nums[i].classList.remove("selected");
                for(let j=0; j<selectNum.length; j++)
                {
                    if(selectNum[j] == parseInt(nums[i].value))
                    {
                        selectNum.splice(j, 1);
                    }
                }
                console.log(selectNum);
            }
        });
    }

    const doors = document.querySelectorAll(".door");              // 각 숫자 
    document.querySelector("#spinner").addEventListener("click", spin);
    document.querySelector("#reseter").addEventListener("click", init);
    document.querySelector("#reseter").addEventListener("click", reset);
    document.querySelector("#hinter").addEventListener("click", showHint);

    async function spin() {
        cnt = 0;   //pools 내의 pool 순차적 처리용
        if(selectNum.length < 6) // 이용자 선택 숫자 개수 확인
        {
            alert(`숫자 ${selectNum.length}개를 선택했습니다. \n숫자 6개를 선택하세요.`); 
            return;
        } else if (selectNum.length > 6)
        {
            alert(`숫자 ${selectNum.length}개를 선택했습니다. \n숫자 6개를 선택하세요.`); 
            return;
        }

        init(false, 2);                             // 초기화(false=아무 일도 안 함, duration=애니메이션1초)
        for ( const door of doors)                  // 숫자 안의
        {                                
            const boxes = door.querySelector(".boxes");                      // boxes 클래스 선택하여
            const duration = parseInt(boxes.style.transitionDuration);      // 지정된 애니메이션 시간 가져와
            boxes.style.transform = "translateY(0)";                        // boxes를 세로 위끝으로 설정 -> 최종 위치???
            await new Promise((resolve) => setTimeout(resolve, duration * 100));  // ??? 0.1초씩 지연시킴
        }
        setTimeout(check, 2000);
    }
    
    function init(firstInit = true, duration = 1) {
        for (const door of doors) 
        {         
            if (firstInit)                          
            {                        
                door.dataset.spinned = "0";          // data-spinned -> 0 으로 설정(초기화???)
            } else if (door.dataset.spinned === "1") // data-spinned -> 1이면(추첨이 끝났으면)
            {  
                return;                             // 아무 것도 안 함
            }
    
            const boxes = door.querySelector(".boxes");  // boxes를
            const boxesClone = boxes.cloneNode(false);  // 복제. 왜???? 해당 node의 children 까지 복제하려면 true, 해당 node 만 복제하려면 false
    
            if (!firstInit)                 // firstInit -> false이면 
            {        
    
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
            
            let pool = pools[cnt];
            cnt += 1;
            // console.log(pool);
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

    function check()      // 당첨 확인
    {
        let wins = 0;
        let bonus = false;
        console.log(lotte, selectNum);
        for ( let i=0; i<selectNum.length; i++ ) 
        {
            // console.log(selectNum[i].value, typeof(selectNum[i].value))
            if( lotte.includes( selectNum[i] ) )
                wins += 1;
            if( bonusNum == selectNum[i] )
                bonus = true;
        }
        console.log("맞춘 개수 =", wins);
        if (wins == 6) {
            alert("1등");
        } else if(wins == 5 && bonus) {
            alert("2등");
        } else if (wins == 5) {
            alert("3등");
        } else if (wins == 4) {
            alert("4등");
        } else if ( wins == 3) {
            alert("3등");
        } else {
            alert("꽝")
        }
    }

    function reset()   // 다시 시작
    {
        location.reload();
    }
    
    let h = 0; // 힌트 보여줄 인덱스
    function showHint() // 힌트 보여주기
    {
        if(h<5)
        {
            let hint = document.querySelector(".hint");
            let span = document.createElement("span");
            span.classList.add("hintNum");
            span.innerText = lotte[h];
            hint.appendChild(span);
            h++;
        } else { alert("더 이상의 힌트는 없습니다."); }
    }


    init();
})();
