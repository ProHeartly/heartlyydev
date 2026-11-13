
document.addEventListener("DOMContentLoaded", () => {
    const box = document.createElement("dialog");
    box.className = "zoom";
    box.innerHTML = '<img alt="">';
    document.body.append(box);

    const big = box.querySelector("img");
    let small = null;

    function swap(change) {
        if (!document.startViewTransition) return change();
        return document.startViewTransition(change).finished;
    }

    function open(img) {
        small = img;
        big.src = img.src;
        big.alt = img.alt;

        small.style.viewTransitionName = "zoom";
        swap(() => {
            small.style.viewTransitionName = "";
            big.style.viewTransitionName = "zoom";
            box.showModal();
        });
    }

    function close() {
        const done = swap(() => {
            big.style.viewTransitionName = "";
            small.style.viewTransitionName = "zoom";
            box.close();
        });
        Promise.resolve(done).then(() => small.style.viewTransitionName = "");
    }
    document.querySelectorAll(".paper-main img, .photo img").forEach(img => {
        img.addEventListener("click", () => open(img))
    });

    box.addEventListener("click", close);

    box.addEventListener("cancel", e=> {
        e.preventDefault();
        close();
    });
});