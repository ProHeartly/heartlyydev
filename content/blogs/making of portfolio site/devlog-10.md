# Small tweakz

I had some cool ideaz:
Let's add two new sections in the home page, one for a dino game.. so Basically a while back, I had made a [dino game](https://github.com/ProHeartly/dino) which was completely offline thingy, and it was like url based game which worked just by pasting a code in any browser, and under the hood, its a isolated html file, so why don't I make a page for playing that game! would be cool, won't it?

and I will leave another one nothing for now.. tbd what to put.

# Progress:
1) making a dino game (not acutally making it but kinda keeeping it into our site):
Since, on the actual project, i had size limit of 3kb but here, we don't really have that, SOOOO I will be adding more features here.. starting from making custom pallet for dark and light mode for game.
![alt text](/images/image31.png)
![alt text](/images/image32.png)

*dino is going to hug his friend cactus :D*

2) small qol: fixed the underline under the icon in `blog page` while hovering <br>
from this:
![alt text](/images/image33.png)
to this:
![alt text](/images/image34.png)
and added this feature also in `about me` page also in `gallery` page.

3) Made the pause screen which is at the begining before any input and when pressed esc.
![alt text](/images/image35.png)

4) Made the game's theme change in sync with site: before, the change in theme in game used to occur only after the next update, and in case of paused screen, only after unpause but now it happens in the real time by using
`observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });`, this looks for change in the `data-theme` and changes the theme of game real-time in sync.
![alt text](/images/image36.png)

5) Offline dino:
YAHHH kinda unique thingyy.. since we alr have the dino game, let's make the browser save a cache of dino game on their first visit, then when they visit offline, the game will load instead of errors :D. This can be done using service worker.

I will put a small code inside `theme.js`, **WHY THEME.JS??**: cuz it's in almost all site (from what i can remember), so it perfectly fits the requirement to initilize the service worker download. I used [this](https://web.dev/articles/offline-fallback-page?hl=en) as a source of info and other sources like yt too :D

Although, now it works but, I had few qol ideas: like in offline, the ph icons doesn't load, so maybe i have to create alternative text for them and also, there is no indication for the user that he is offline, this might lead to misunderstandings. So we have to fix this stuff!

*ANOTEHR PROBLEM*: So I deployed it into nest to test out in actual not just local and when i tried offline thingy, it always said server issue even when it was just no internet SO i have to change how no internet is detected!

![alt text](/images/image37.png)

Turns out `navigator.onLine` is not very reliable but we can use `generate_204` from google to check the same thing, from `https://www.google.com/generate_204`

YAH! now it works!
![alt text](/images/image38.png)