const shelf = document.querySelector(".shelf");
const books = document.querySelectorAll(".book");

books.forEach(book => {
    book.addEventListener("click", e => {
        if (e.target.closest("a")) return; // so the demo n github button works as link

        const wasOpen = book.classList.contains("open");
        books.forEach(b => b.classList.remove("open"));

        if (!wasOpen) {
            book.classList.add("open");
            setTimeout(() => book.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" }), 350);
        }
    });
});

shelf.addEventListener("wheel", e => {
    if (shelf.scrollWidth <= shelf.clientWidth) return; // if everything fits, scroll the page as usual
    e.preventDefault();
    shelf.scrollLeft += e.deltaY;
}, { passive: false });