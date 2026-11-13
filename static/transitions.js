
window.addEventListener("pagereveal", e => {
    if (!e.viewTransition || !window.navigation) return;

    const from = new URL(navigation.activation.from.url).pathname;
    const to = new URL(navigation.activation.entry.url).pathname;

    if (from === "/") {
        e.viewTransition.types.add("from-home");
    }
    if (to === "/") {
        e.viewTransition.types.add("to-home");
    }
});