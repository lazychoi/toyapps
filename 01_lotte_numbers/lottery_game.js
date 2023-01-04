let lotte = new Array();

function choose()
{    
    let num = Math.floor(Math.random() * 45) + 1; 
    return num;
}

while(lotte.length < 7)
{
    let tmp = choose();
    if ( !lotte.includes(tmp) )
        lotte.push(tmp)
}
const bonusNum = lotte.splice(6, 1)
console.log(lotte, bonusNum)

const user = document.querySelectorAll(".user")
const btns = document.querySelectorAll(".btn")
btns[0].addEventListener("click", check )

let wins = 0;
let bonus = false;
function check()
{
    for ( let i=0; i<user.length; i++ ) 
    {
        // console.log(user[i].value, typeof(user[i].value))
        if( lotte.includes( parseInt(user[i].value) ) )
            wins += 1;
        if( bonusNum == parseInt(user[i].value) )
            bonus = true;
    }
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
