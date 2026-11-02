const email = ["rasimmahatoo", "gmail.com"].join("@") // put together like this so scrapers cannot spam it ;-;

const contacts = [
    { name: "github", icon: "ph-github-logo", handle: "@ProHeartly", act: "link", link: "https://github.com/proheartly" },
    { name: "mail", icon: "ph-envelope-simple", handle: email, act: "copy", copy: email },
    { name: "hackatime", icon: "ph-timer", handle: "my coding hours", act: "link", link: "https://hackatime.hackclub.com/@rasim" },
    { name: "linkedin", icon: "ph-linkedin-logo", handle: "Rasim", act: "link", link: "https://www.linkedin.com/in/heartly/" },
    { name: "discord", icon: "ph-discord-logo", handle: "@heartlyplayz", act: "link", link: "https://discord.com/users/878215711779090443" },
    { name: "hackclub slack", icon: "ph-slack-logo", handle: "@Heartly", act: "link", link: "https://hackclub.enterprise.slack.com/team/U0A4016A14N" },
    { name: "msg me", icon: "ph-chat-circle-dots", handle: "straight to my inbox", act: "write", message: true }
];

const dial = document.querySelector(".dial");
const ring = document.querySelector(".ring");
const card = document.querySelector(".card");
const center = document.querySelector(".center");
const stop = document.querySelector(".stop");
const step = 360 / contacts.length;
const openedAt = Date.now();

let angle = 0;
let picked = -1;

const holes = contacts.map((c, i) => {
    const hole = document.createElement("button");
    hole.className = "hole";
    hole.dataset.i = i;
    hole.innerHTML = `<i class="ph-duotone ${c.icon}"></i>`;
    hole.setAttribute("aria-label", c.name);

    const a = (i * step - 90) * Math.PI / 180;
    hole.style.left = 50 + 37 * Math.cos(a) - 11 + "%";
    hole.style.top = 50 + 37 * Math.sin(a) - 11 + "%";

    ring.appendChild(hole);
    return hole;
});

function draw() {
    ring.style.transform = `rotate(${angle}deg)`;
    holes.forEach(h => h.firstChild.style.transform = `rotate(${-angle}deg)`);
}

function showCard() {
    const i = ((Math.round(-angle / step) % contacts.length) + contacts.length) % contacts.length;

    if (i===picked) return;
    picked = i;

    const c = contacts[i];
    card.innerHTML = `
        <h2>${c.name}</h2>
        <span class="handle">${c.handle}</span>
        <button class="act">${c.act}</button>
    `;

    holes.forEach((h, n) => h.classList.toggle("on", n===i));
    center.innerHTML = `<i class="ph-duotone ${c.icon}"></i>`;

    card.classList.remove("fade");
    stop.classList.remove("tick");
    void card.offsetWidth; // restart the anim
    card.classList.add("fade");
    stop.classList.add("tick");

    const btn = card.querySelector(".act");
    btn.addEventListener("click", ()=> {
        if (c.link) window.open(c.link, "_blank");
        if (c.message) openMessage(btn);
        if (c.copy) {
            navigator.clipboard.writeText(c.copy);
            btn.textContent = "copied mail";
            setTimeout(() => btn.textContent = c.act, 1200)
        }
    });
}

function spinTo(target) {
    const from = angle;
    const to = from + ((((target - from) % 360) + 540) %360 - 180);
    const start = performance.now();

    function frame(now) {
        const t = Math.min(1, (now - start) /450);
        angle = from + (to - from) * (1 - (1 -t ) ** 3);
        draw();
        if (t < 1) requestAnimationFrame(frame);
        else showCard();
    }
    requestAnimationFrame(frame);
}

function pointerAngle(e) {
    const r = dial.getBoundingClientRect();
    return Math.atan2(e.clientY - r.top -r.height / 2, e.clientX - r.left -r.width /2) * 180 / Math.PI;
}

let dragging = false;
let dragged = false;
let pressed = null;
let startPointer = 0;
let startAngle = 0;

ring.addEventListener("pointerdown", e => {
    dragging = true;
    dragged = false;
    pressed = e.target.closest(".hole");
    startPointer = pointerAngle(e);
    startAngle = angle;
    ring.setPointerCapture(e.pointerId);
});

ring.addEventListener("pointermove", e => {
    if (!dragging) return;
    const moved = ((pointerAngle(e) - startPointer) % 360 + 540) % 360 - 180;
    if (Math.abs(moved) > 3) dragged = true;
    angle = startAngle + moved;
    draw();
    showCard();
});

ring.addEventListener("pointerup", () => {
    dragging = false;
    if (dragged) spinTo(Math.round(angle / step) * step);

    else if (pressed) spinTo(-pressed.dataset.i * step);
});

dial.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") spinTo(Math.round(angle / step) * step - step);
    if (e.key === "ArrowLeft") spinTo(Math.round(angle / step) * step + step);
});

function openMessage(btn) {
    card.querySelector(".handle").remove();
    btn.replaceWith(document.querySelector("#message-box").content.cloneNode(true));

    const form = card.querySelector(".message");
    form.querySelector("textarea").focus();

    form.addEventListener("submit", async e => {
        e.preventDefault();
        const send = form.querySelector(".act");
        send.disabled = true;
        send.textContent = "sending..";

        const data = new FormData(form);
        data.append("seconds", (Date.now() - openedAt) / 1000);

        const res = await fetch("/contact", { method: "POST", body: data });
        if (res.ok) {
            form.innerHTML = "<p>SENT! thanks for dropping by</p>"
        } else {
            send.disabled = false;
            send.textContent = res.status === 429 ? "too many, try later" : "didn't send, try again";
        }
    });
}

draw();
showCard();