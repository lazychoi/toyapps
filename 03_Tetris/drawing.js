function draw_grid(ctx, minor, major, stroke, fill){
    minor = minor || 10;            // 격자선 간격. default 10 when minor is not given. 
    major = major || minor * 5;     // 굵은 격자선 간격
    stroke = stroke || '#00FF00';   // 격자선 색
    fill = fill || '#009900';       // 글자 색
    ctx.save();                     // save context state for restoring
    ctx.strokeStyle = stroke;
    ctx.fillStyle = fill;
    let width = ctx.canvas.width, height = ctx.canvas.height;

    for(let x=0; x<width; x+=minor){
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.lineWidth = ( x % major == 0 ) ? 0.5 : 0.25;
        ctx.stroke();
        if( x % major == 0 ) { ctx.fillText(x, x, 10); }
    }

    for(let y=0; y<height; y+=minor){
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.lineWidth = (y % major == 0) ? 0.5 : 0.25;
        ctx.stroke();
        if( y % major == 0 ) {ctx.fillText(y, 0, y + 10);}
    }
    ctx.restore();      // restore context state
}

function draw_pacman(ctx, radius, mouth){
    angle = 0.2 * Math.PI * mouth;
    ctx.save();
    ctx.fillStyle = 'yellow';
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.arc(0, 0, radius, angle, -angle);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.restore();
}

function draw_ghost(ctx, radius, options){
    options = options || {};
    let feet = options.feet || 4;
    let head_radius = radius * 0.8;
    let foot_radius = head_radius / feet;
    ctx.save();
    ctx.strokeStyle = options.stroke || 'white';
    ctx.fillStyle = options.fill || 'red';
    ctx.beginPath();
    for(let foot=0; foot<feet; foot++){
        ctx.arc(
            (2*foot_radius * (feet-foot)) - head_radius - foot_radius,
            radius - foot_radius,
            foot_radius, 0, Math.PI
        );
    }
    ctx.lineTo(-head_radius, radius - foot_radius);
    ctx.arc(0, head_radius - radius, head_radius, Math.PI, 2 * Math.PI);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    ctx.restore();
}


// function draw_pacman(ctx, x, y, radius, open){
//     ctx.beginPath();
//     if (open == 0 ) { ctx.arc(x, y, radius, 0, Math.PI * 2); } // 다문 입
//     else if (open == 1){ 
//         ctx.arc(x, y, radius, Math.PI * 0.2, Math.PI * 1.8); 
//         ctx.lineTo(x, y);
//     } 
//     ctx.strokeStyle = 'black';
//     ctx.fillStyle = 'yellow';
//     ctx.fill();
//     ctx.stroke();
// }

function draw_pacman2(ctx){
    //ctx.beginPath();
    let min_radius = 5;
    let max_radius = 50;
    do {
        let x = ctx.canvas.width * Math.random();
        let y = ctx.canvas.height * Math.random();
        let radius = min_radius + (max_radius - min_radius) * Math.random();
        console.log(Math.random(), x, y, radius);
        draw_pacman(ctx, x, y, radius, 1);
    } while (Math.random() < 0.9);
}

function draw_ship(ctx, radius, options){
    options = options || {};
    let angle = (options.angle || 0.5*Math.PI) / 2;
    let curve1 = options.curve1 || 0.25;
    let curve2 = options.curve2 || 0.75;    // 우주선 뒤쪽 커브
    ctx.save();
    if(options.guide){  // 우주선 충돌 감지 반경을 표시하는 원
        ctx.strokeStyle = 'white';
        ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, 2*Math.PI);
        ctx.stroke();
        ctx.fill();
    }
    ctx.lineWidth = options.lineWidth || 2;         // 선 두께
    ctx.strokeStyle = options.stroke || 'white';    // 선 색
    ctx.fillStyle = options.fill || 'black';        // 우주선 색
    ctx.beginPath();
    ctx.moveTo(radius, 0);                          // 중심에서 아래쪽 원 위의 점으로 이동
    ctx.quadraticCurveTo(
        Math.cos(angle) * radius * curve2,
        Math.sin(angle) * radius * curve2,
        Math.cos(Math.PI - angle) * radius,
        Math.sin(Math.PI - angle) * radius
    );
    ctx.quadraticCurveTo(
        -radius * curve1, 
        0,
        Math.cos(Math.PI + angle) * radius,
        Math.sin(Math.PI + angle) * radius
    );
    ctx.quadraticCurveTo(
        Math.cos(-angle) * radius * curve2,
        Math.sin(-angle) * radius * curve2,
        radius,
        0
    );
    ctx.fill();
    ctx.stroke();

    if(options.guide){              // 조절점을 작은 원으로 표시
        ctx.strokeStyle = 'white';
        ctx.fillStyle = 'white';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(                 // 중심에서 우측 위로 조절선 표시 -angle -> -0.25pi
            Math.cos(-angle) * radius,
            Math.sin(-angle) * radius)
        ;     
        ctx.lineTo(0, 0);

        ctx.moveTo(                 // 중심에서 우측 아래로 조절선 표시 angle -> 0.25pi
            Math.cos(angle) * radius,
            Math.sin(angle) * radius)
        ;     
        ctx.lineTo(0, 0);

        ctx.moveTo(-radius, 0)      // 중심에서 왼쪽으로 조절선 표시
        ctx.lineTo(0, 0);
        ctx.stroke();

        ctx.beginPath();            // 우측 하단 조절점 표시
        ctx.arc(
            Math.cos(angle) * radius * curve2,
            Math.sin(angle) * radius * curve2, 
            radius/40, 0, 2*Math.PI
        );
        ctx.fill();
        ctx.beginPath();            // 우측 상단 조절점 표시
        ctx.arc(
            Math.cos(-angle) * radius * curve2,
            Math.sin(-angle) * radius * curve2, 
            radius/40, 0, 2*Math.PI
        );
        ctx.fill();
        ctx.beginPath();            // 좌측 중앙 조절점 표시
        ctx.arc(radius * curve1 - radius, 0, radius/50, 0, 2*Math.PI);
        ctx.fill()
    }
    ctx.restore();
}

function draw_asteroid(ctx, radius, shape, options){
    // 정n각형 그리기 -> noise
    options = options || {};
    ctx.strokeStyle = options.stroke || 'white';
    ctx.fillStyle = options.fill || 'black';
    ctx.save();
    ctx.beginPath();
    for(let i=0; i<shape.length; i++){
        ctx.rotate(2*Math.PI / shape.length);
        ctx.lineTo(radius + radius * options.noise * shape[i], 0);
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    if(options.guide){
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, 2*Math.PI);
        ctx.stroke();
        ctx.beginPath();
        ctx.lineWidth = 0.2;
        ctx.arc(0, 0, radius + radius * options.noise, 0, 2*Math.PI);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(0, 0, radius - radius * options.noise, 0, 2*Math.PI);
        ctx.stroke();
    }
    ctx.restore();
}
