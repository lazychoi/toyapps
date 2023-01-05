console.log("Before timeout: " + new Date());
function f() {
    console.log("After timeout: " + new Date());
}
setTimeout(f, 60*1000);
console.log("I happen after setTimeout");
console.log("Me too.");


function countdown(){
    let i;
    console.log("Countdown");
    for(i=5;i>=0;i--){
        setTimeout(function() {
            console.log(i===0?"GO!":i);
        }, (5-i)*1000);
    }
}
countdown();


const fs = require('fs');
const fname = 'may_or_ma_not_exsit.txt';
fs.readFile(fname, function(err, data){
    if(err) return console.err(`error reading file ${fname} : ${err.message}`);
    console.log(`${fname} contents: ${data}`);
});


function countdown(seconds){
    return new Promise( function(resolve, reject) {
        for(let i=seconds; i>=0; i--){
            setTimeout(function() {
                if(i>0) console.log(i + '...');
                else resolve(console.log("GO!"));
            }, (seconds-i)*1000)
        }
    });
}
countdown(5);

