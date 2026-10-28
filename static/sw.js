// THIS IS SERVICE WORKER: aka this keeps the dino game saved in brower to be playable even when offline.
// source: https://web.dev/articles/offline-fallback-page?hl=en
const CACHE = "dino-v1"; // I need to change this if i update dino.html or theme.js


// first visit: save the game in da browser
self.addEventListener("install", event => {
    event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(["/dino", "/static/theme.js"])));
});

// a new version took over: update saved copies
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))
        )
    );
});

// chek if no internet or server is down and show the game
self.addEventListener("fetch", event => {
    const request = event.request;

    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request)
                .then(response => response.status >= 500 ? caches.match("/dino"): response)
                .catch(() => caches.match("/dino"))
        );
    }

    if (request.url.endsWith("/static/theme.js")) {
        event.respondWith(fetch(request).catch(() => caches.match(request)));
    }
});