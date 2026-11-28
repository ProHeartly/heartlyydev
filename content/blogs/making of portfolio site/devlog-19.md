# Fixes

1) The caching on mobiles are very subborn.. like IT WASN'T updating no matter what i didd.... so i implemented a server side fixx

**First attempt:**

`src.env.globals["v"] = int(time.time())` this line initiates a global variable `v` which is equal to `time.time()`: which is the time of deploy, so like everytime i deploy, the `v` changes. And when calling for style or js files, i added `?v={{ v }}` this at back, which means everytime the server redeploys, the `v` changes and so the browser asks for new file instead of relying on old one.

**Problemmmm:** But what happened wasss i would have to replace each page with that thing on each resource that I called.. so lets look for alternative

**Another attempt:**

```python
class RevalidateStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
        return response

app.mount("/static", RevalidateStaticFiles(directory="static"), name="static")
```

using this `no-cache` and `must-revalidate` headers makes so that browser looks for any update in resource.

**PROBLEMMMM:** It should have workedd in theoryyy but dk why it didn't work in my case, as soon as I removed html part, my mobile version went back to very old version.. the horizontal layout one (very old version), I even tried purging the cache in cloudflare and even invalidate everything option but no luckkk

**Anotherrr fixx:** Hmmm what I thought was if somehow we could add the `?v={{ v }}` thingy without replacing every html.

`@app.middleware("http")` this registers a wrapper function in fastapi that intercepts every incomming HTTP request before it reaches routes and every outgoing response before it goes back to browser.

then I checked for `text/html` which means we are only looking for the `/static/*.css` or `/static/*.js` and we further isolate the search with `r'(/static/[^"\']+\.(?:css|js))(?=["\'])'`, which might look complex at first but simply:

* find something that starts with `/static/`
* keep going until it hits quote (" or ') which is checked by `[^"\']+` part
* it must end in `.css` or `.js`
* and the next character has to be a quote (so it only takes the exact url) and also its done with lookahead: `(?=["\'])` so it checks but doesn't include it

with this thingy, `/static/style.css` gets matched but `/static/logo.png` doesn't..

then finally, `rf'\1?v={BOOT_V}'` this puts the `?v=` thingy for rechecking cachee

2) Fixed the text not being readable in the `.record` thingy

In dark theme, when the album cover of song was yellow colored, then the text would be unreadable soo for fixing it, I added `filter: brightness(0.5) contrast(1.1);` to `.label` which makes the album art little darker. And I also added `filter: drop-shadow(0 2px 4px rgba(7, 11, 30, 0.95));` to `.track-front` which is the text on front, so now it's moree visible with those drop shadows

**small fix:** I also made the text size smaller so most text fits.

![alt text](/images/image81.png)