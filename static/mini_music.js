document.addEventListener("DOMContentLoaded", () => {
    const API_KEY = "330216c7221b68e42208f36c509eba8b"; // Exposing API key doesn't do anythign in this case so well
    const USERNAME = "heartlye";

    const trackBackEl = document.getElementById("track-back");
    const trackFrontEl = document.getElementById("track-front");
    const recordEl = document.getElementById("record");
    const labelEl = document.getElementById("label");
    const what = document.getElementById("what");

    const listenBtn = document.getElementById("listen-btn");
    const listenText = document.getElementById("listen-text");
    const listenIcon = document.getElementById("listen-icon");
    const ring = document.getElementById("ring-progress");
    const fullSong = document.getElementById("full-song");
    const RING = 502.65;

    const audio = new Audio();
    audio.volume = 0.4;
    let preview = null;

    let lastTrackKey = "";

    function updateTrackText(text) {
        trackBackEl.textContent = text;
        trackFrontEl.textContent = text;
    }

    function setButton(icon, text) {
        listenIcon.className = "ph-duotone " + icon;
        listenText.textContent = text;
    }

    async function loadPreview(trackName, artist) {
        preview = null;
        fullSong.innerHTML = "";
        fullSong.classList.remove("show");
        ring.style.strokeDashoffset = RING;

        const res = await fetch(`/api/preview?song=${encodeURIComponent(trackName)}&artist=${encodeURIComponent(artist)}`);
        const data = await res.json();
        if (!data.preview) return;

        preview = data.preview;
        setButton("ph-play", "Listen along");

        const names = { spotify: "Spotify", youtube: "YouTube", appleMusic: "Apple Music" };
        fullSong.innerHTML = "full song on";
        for (const key in data.links) {
            fullSong.innerHTML += ` <a href="${data.links[key]}" target="_blank">${names[key]}</a>`;
        }
    }

    function setPlaying(trackName, albumArtUrl, artist) {
        if (trackName === lastTrackKey || !audio.paused) return;
        lastTrackKey = trackName;

        updateTrackText(trackName);

        recordEl.classList.add("playing");

        labelEl.style.backgroundImage = `url("${albumArtUrl}")`;

        setButton("ph-play", "Search this song");

        what.classList.remove("hidden");

        loadPreview(trackName, artist)
    }

    function setIdle() {
        if (!audio.paused) return;
        preview = null;
        fullSong.innerHTML = "";

        updateTrackText("Not listening to anything");

        recordEl.classList.remove("playing");

        labelEl.style.backgroundImage = `none`;

        lastTrackKey = "";

        setButton("ph-arrow-square-out", "Check last.fm profile");

        what.classList.add("hidden");
    }

    async function fetchNowPlaying() {
        const endpoint = `https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=${USERNAME}&api_key=${API_KEY}&format=json&limit=1`;
        const response = await fetch(endpoint);

        const data = await response.json();
        const latestTrack = data?.recenttracks?.track?.[0];

        if (!latestTrack) {
            setIdle();
            return;
        }

        const isNowPlaying = latestTrack["@attr"]?.nowplaying === "true";

        if (isNowPlaying) {
            const trackName = latestTrack.name || "Unknown song";
            const artist = latestTrack.artist["#text"];
            const albumArtUrl = latestTrack.image?.find((img) => img.size === "extralarge")?.["#text"] || "";

            setPlaying(trackName, albumArtUrl, artist);
        } else {
            setIdle();
        }
    }

    listenBtn.addEventListener("click", () => {
        if (preview) {
            if (audio.paused) {
                if (audio.src !== preview) audio.src = preview;

                audio.play();
                setButton("ph-pause", "Pause");
                fullSong.classList.add("show");
            } else {
                audio.pause();
                setButton("ph-play", "Resume");
            }
            return;
        }
        const trackName = trackBackEl.textContent.trim();

        if (trackName && trackName !== "Connecting..." && trackName !== "Not listening to anything") {
            const ytSearchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(trackName)}`;
            window.open(ytSearchUrl, "_blank", "noopener,noreferrer");
        } else {
            window.open(`https://www.last.fm/user/${USERNAME}`, "_blank", "noopener,noreferrer");
        }
    });

    audio.addEventListener("timeupdate", () => {
        ring.style.strokeDashoffset = RING * (1 - audio.currentTime / audio.duration);
    });

    audio.addEventListener("ended", () => {
        ring.style.strokeDashoffset = RING;
        setButton("ph-play", "Listen along");
    });

    document.addEventListener("visibilitychange", () => {
        if (document.hidden && !audio.paused) {
            audio.pause();
            setButton("ph-play", "Resume");
        }
    })

    fetchNowPlaying();
    setInterval(fetchNowPlaying, 10000);
});