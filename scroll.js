document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".main");

    container.addEventListener("wheel", (e) => {
        e.preventDefault();
        container.scrollLeft += e.deltaY ;
    }, {passive: false});
});