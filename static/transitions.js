
window.addEventListener("pagereveal", e => {
    if (!e.viewTransition || !window.navigation) return;

    const from = new URL(navigation.activation.from.url).pathname;
    if (from === "/") {
        e.viewTransition.types.add("from-home");
    }
});