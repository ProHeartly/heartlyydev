document.addEventListener("DOMContentLoaded", () => {
    const API_KEY = "330216c7221b68e42208f36c509eba8b"; // Exposing API key doesn't do anythign in this case so well
    const USERNAME = "heartlye";

    const trackBackEl = document.getElementById("track-back");
    const trackFrontEl = document.getElementById("track-front");
    const recordEl = document.getElementById("record");
    const labelEl = document.getElementById("label");

    let lastTrackKey = "";

    function updateTrackText(text) {
        trackBackEl.textContent = text;
        trackFrontEl.textContent = text;
    }

    function setPlaying(trackName, albumArtUrl) {
        if (trackName === lastTrackKey) return;
        lastTrackKey = trackName;

        updateTrackText(trackName);

        recordEl.classList.add("playing");

        labelEl.style.backgroundImage = `url("${albumArtUrl}")`;

    }

    function setIdle() {
        updateTrackText("Not listening to anything");

        recordEl.classList.remove("playing");

        labelEl.style.backgroundImage = `none`;

        lastTrackKey = "";
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
            const albumArtUrl = latestTrack.image?.find((img) => img.size === "extralarge")?.["#text"] || "";

            setPlaying(trackName, albumArtUrl);
        } else {
            setIdle();
        }
    }

    fetchNowPlaying();
    setInterval(fetchNowPlaying, 10000);
});