document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".main");

    let scrollPos = container.scrollLeft;
    let velocity = 0;
    let isAnimating = false;

    function Animate() {
        if (!isAnimating) return;

        velocity *= 0.92; // This is friction / damping
        scrollPos += velocity;

        const maxScroll = container.scrollWidth - container.clientWidth;

        if (scrollPos<0) {
            scrollPos = 0;
            velocity = 0;
        } else if (scrollPos > maxScroll) {
            scrollPos = maxScroll;
            velocity = 0;
        }

        container.scrollLeft = scrollPos;

        if (Math.abs(velocity) > 0.1) {
            requestAnimationFrame(Animate);
        } else {
            isAnimating = false;
        }
    }

    container.addEventListener("wheel", (e) => {
        if (window.innerWidth <= 700) return;
        e.preventDefault();

        if (!isAnimating) {
            scrollPos = container.scrollLeft
        }

        velocity += e.deltaY * 0.18; // kinda like momentum

        if (!isAnimating) {
            isAnimating = true;
            requestAnimationFrame(Animate);
        }
    }, {passive: false});
});