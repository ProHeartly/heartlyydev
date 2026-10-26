const grid = document.querySelector(".grid");
const buttons = document.querySelectorAll(".levels button");

function apply(level) {
    grid.className = "grid " + level;
    buttons.forEach(b => b.classList.toggle("active", b.dataset.level === level));
}

function setLevel(level) {
    if (document.startViewTransition) {
        document.documentElement.classList.add("morphing");
        const transition = document.startViewTransition(() => apply(level));
        transition.finished.then(() => document.documentElement.classList.remove("morphing"));
    } else {
        apply(level)
    }
}

buttons.forEach(button => {
    button.addEventListener("click", () => setLevel(button.dataset.level));
});

apply("l1")