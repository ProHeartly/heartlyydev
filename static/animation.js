document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");
    const container = document.querySelector(".main");

    const observer = new IntersectionObserver(entries => {
        let i = 0;
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.setProperty("--delay", `${i * 0.08}s`);
                entry.target.classList.add("in-view");
                i++;
            } else {
                entry.target.classList.remove("in-view");
            }
        });
    }, {root: container, threshold: 0.15});

    cards.forEach(card => observer.observe(card));
});