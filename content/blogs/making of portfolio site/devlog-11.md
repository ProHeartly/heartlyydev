# Mobile friendlyyy, finally! and LISTEN along feature in now playing thingy

Sooo, after alot of comments from my friends about the site not being mobile friendly aka responsive, I will be making this mobile responsivee!!

And another veryy suggested thing was listen along, like listen to the song which is being played by me at that moment!

# Progress:
1) Starting with da homepage:
instead of making it scroll down like generally what most website do, i even made scroll side wise for mobile too :D
![alt text](/images/image39.png)

Another thing that i changed was:
`root: container` to `root: window.innerWidth > 700? container : null` since in mobile, i experienced little stucking like thingy when scrolling.

And I added `if (window.innerWidth <= 700) return;` to scroll.js to make phones scroll normally.

2) About section and gallery:
First of all a small tweak, I added `theme-icon` to `gallery` section.
and here's how both look in mobile.
![alt text](/images/image40.png)
![alt text](/images/image41.png)
and you can see that small `theme-icon` in the gallery section :D

3) Listen along!!
Sooo the idea was, when I'm listening to song, you can press a button and hear it too. My music card already knew what I'm playing (thanks to last.fm), so now I just needed a way to actually play the song. Problem was, I can't just host full songs on my site (due to copyright so yah), so I tested and tested and tested..

**Attempt 1: Youtube**
Youtube was my first choice when I thought of this but turns out it is so mcuh hard to do it with youtube cuz youtube requires the iframe to be atleast 200x200px and I couldn't find a way around this!

**Attempt 2: Itunes**
iTunes has a free search with previews, so I made a route in `main.py`:
`/api/preview?song=...&artist=...`
...and it returned nothing. Like literally `"resultCount": 0`, even for Blinding Lights 💀
Even forcing the US store with `&country=us` gave 0. Turns out Apple just doesn't answer requests from my network.

**Attempt 3: Deezer**
Switced to deezer, which also has free previews and no API key needed. AND IT ACUTALLY WORKED! soo yah can't play the whole music but can play a preview.

**Small things I learned:**
* I also wanted "full song on Spotify / Youtube / Apple Music" links, so I tried `song.link` to ifnd the song on every app. It gave me `401: Unauthorized` T_T  SO instead I just set link to each app's *search page* for that song.
* Deezer preview links *expires after 15 min* (the exp time is literally inside the link: `exp=..`). So my server only remembers each song for *10 min* (just for a safe margin), then re-requests


Yah finally! now it works after so many breaking and building!!!!
![alt text](/images/image42.png)

I wish I could tell yall HOW happy I'm completing this!!! well.. and I also tried new style of devlog.