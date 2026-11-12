document.addEventListener("DOMContentLoaded", () => {
    const page = document.scrollingElement;

    let pos = page.scrollTop;
    let velocity = 0;
    let moving = false;

    function animate() {
        velocity *= 0.92; // friction, same as home page
        pos += velocity;

        const max = page.scrollHeight - window.innerHeight;
        if (pos < 0 || pos > max) {
            pos = Math.max(0, Math.min(max, pos));
            velocity = 0;
        }

        page.scrollTop = pos;

        if (Math.abs(velocity) > 0.1) {
            requestAnimationFrame(animate);
        } else {
            moving = false;
        }
    }

    window.addEventListener("wheel", e => {
        if (e.ctrlKey || Math.abs(e.deltaY) < 40) return;
        e.preventDefault();

        if (!moving) {
            pos = page.scrollTop;
            moving = true;
            requestAnimationFrame(animate);
        }

        velocity += e.deltaY * 0.18;
    }, {passive: false})
});