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

function draw_pacman(ctx, x, y, radius, open){
    ctx.beginPath();
    if (open == 0 ) { ctx.arc(x, y, radius, 0, Math.PI * 2); } // 다문 입
    else if (open == 1){ 
        ctx.arc(x, y, radius, Math.PI * 0.2, Math.PI * 1.8); 
        ctx.lineTo(x, y);
    } 
    ctx.strokeStyle = 'black';
    ctx.fillStyle = 'yellow';
    ctx.fill();
    ctx.stroke();
}

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