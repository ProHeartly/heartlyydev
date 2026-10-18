document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");
    const container = document.querySelector(".main");

    cards.forEach((card, index) => {
        card.style.transitionDelay = `${(index * 0.1).toFixed(2)}s`;
    });

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("in-view");
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: container,
        threshold: 0.15
    });
    cards.forEach(card => observer.observe(card));
});