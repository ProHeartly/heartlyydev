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