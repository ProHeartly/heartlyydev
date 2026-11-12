document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");
    const container = document.querySelector(".main");

    // like how fast its scrolling, in unit of pixels per millisecond
    let speed = 0;
    let lastX = container.scrollLeft;
    let lastT = performance.now();

    container.addEventListener("scroll", () => {
        const now = performance.now();
        const v = Math.abs(container.scrollLeft - lastX) / Math.max(1, now - lastT);
        speed = speed * 0.6 + v * 0.4; // smooth it so one jumpy frame doesn't count
        lastX = container.scrollLeft;
        lastT = now;
    });

    const observer = new IntersectionObserver(entries => {
        // stopped scrolling for a bit? then its really not that fast any more
        const fast = performance.now() - lastT < 150 ? speed : 0;
        //  1 = full slow animation, 0.3 = fastest (about like 3x quicker)
        const pace = Math.max(0.3, 1 / (1 + fast * 0.2));

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const x = entry.boundingClientRect.left / window.innerWidth;
                entry.target.style.setProperty("--delay", `${Math.max(0, x) * 0.5 * pace}s`);
                entry.target.style.setProperty("--pace", pace);
                entry.target.classList.add("in-view");
            } else {
                entry.target.classList.remove("in-view");
            }
        })
    }, {root: window.innerWidth > 700? container : null, threshold: 0.15});

    cards.forEach(card => observer.observe(card));
});