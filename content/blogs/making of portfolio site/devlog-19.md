# Fixes

1) The caching on mobiles are very subborn.. like IT WASN'T updating no matter what i didd.... so i implemented a server side fixx

`src.env.globals["v"] = int(time.time())` this line initiates a global variable `v` which is equal to `time.time()`: which is the time of deploy, so like everytime i deploy, the `v` changes. And when calling for style or js files, i added `?v={{ v }}` this at back, which means everytime the server redeploys, the `v` changes and so the browser asks for new file instead of relying on old one.