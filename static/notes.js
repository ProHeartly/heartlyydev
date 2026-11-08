const canvas = document.querySelector(".canvas");
const world = document.querySelector(".world");

let panX = 0;
let panY = 0;
let lastX = null;
let lastY = null;

const gap = 24;
const placed = []

function isFree(x, y, w, h) {
    return placed.every(p => 
        Math.abs(p.x - x) >= (p.w + w) / 2 + gap ||
        Math.abs(p.y - y) >= (p.h + h) / 2 + gap
    );
}


// if the spot is taken, go round in bigger and bigger circles till we find a free one
function findSpot(x, y, w, h) {
    for (let r = 0; ; r += 40) {
        for (let a = 0; a < 360; a += 30) {
            const nx = x + r * Math.cos(a * Math.PI / 180);
            const ny = y + r * Math.sin(a * Math.PI / 180);
            if (isFree(nx, ny, w, h)) return { x: nx, y: ny};
        }
    }
}


notes.forEach((n, i) => {
    const note = document.createElement("div");
    note.className = "note";
    note.style.rotate = (i * 37 % 9) - 4 + "deg";
    const text = document.createElement("p");
    text.textContent = n.text;
    const sign = document.createElement("span");
    sign.className = "sign";
    sign.textContent = "- " + n.name;
    note.append(text, sign)
    world.appendChild(note);

    const w = note.offsetWidth;
    const h = note.offsetHeight;

    const spot = findSpot(n.x, n.y, w, h);
    placed.push({ x: spot.x, y: spot.y, w, h });

    note.style.left = spot.x - w / 2 +"px";
    note.style.top = spot.y - h / 2 + "px";
});

function move() {
    const x = panX + innerWidth / 2;
    const y = panY + innerHeight / 2;
    world.style.transform = `translate(${x}px, ${y}px)`;
    canvas.style.backgroundPosition = `${x}px ${y}px`;
}

canvas.onpointerdown = e => {
    lastX = e.clientX;
    lastY = e.clientY;
    canvas.setPointerCapture(e.pointerId);
};

canvas.onpointermove = e => {
    if (lastX === null) return;
    panX += e.clientX - lastX;
    panY += e.clientY - lastY;
    lastX = e.clientX;
    lastY = e.clientY;
    move();
}

canvas.onpointerup = () => lastX = null;

canvas.onwheel = e => {
    e.preventDefault();
    panX -= e.deltaX;
    panY -= e.deltaY;
    move();
};

window.onresize = move;
move();