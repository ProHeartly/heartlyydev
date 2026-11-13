
window.addEventListener("pagereveal", e => {
    if (!e.viewTransition || !window.navigation) return;

    const from = new URL(navigation.activation.from.url).pathname;
    const to = new URL(navigation.activation.entry.url).pathname;

    if (from === "/") {
        e.viewTransition.types.add("from-home");
    } else if (to === "/") {
        e.viewTransition.types.add("to-home");
    } else if (from.startsWith("/blogs") && to.startsWith("/blogs")) {
        const depth = path => path.split("/").filter(Boolean).length; // /blogs = 1, /blogs/devlogs = 2, /blogs/devlogs/devlog-1 = 3
        e.viewTransition.types.add(depth(to) < depth(from) ? "blog-out": "blog-in");
    }
});