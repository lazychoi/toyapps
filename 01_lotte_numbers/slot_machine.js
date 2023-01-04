(function() {
"use strict"

// 하단에 추첨 기호 표시
const items = []
for(let i=1; i<46; i++)
    items[i] = i;

document.querySelector(".info").textContent = items.join(' ');

const doors = document.querySelectorAll(".door");
document.getElementById("spinner").addEventListener("click", spin);
document.getElementById("reseter").addEventListener("click", init);

async function spin() {
    S
}


})();