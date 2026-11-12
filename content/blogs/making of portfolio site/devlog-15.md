# Qol updates

**Change 1:** So i noticed when I shared my website in insta or discord, it showed plain link without any embeds or anything so I wanted to add meta tag thingy to make a kinda embeds.

what we can do:
* `title` and `description`: this shows in the tab and in google search result.
* `og:` tags (oepn graph): this is shown by discord, whatsapp, slack, and other platforms to make preview card aka embeds, lie title, description, and a image.
* `twitter:card`: tells x to show the big image version.
* there are others too but those are mostly not needed.

I made a `meta.html` which has all the meta things and every other page just uses
```html
{% set title = "Heartlyy | Gallery" %}
{% set desc = "Hey! check these random photos from my gallery." %}
{% include "meta.html" %}
```
So every page has its own title and description, but the tags are written only once at `meta.html` And for the blog posts, it uses post's own title and summary, so every devlog gets its own preview thingy.

I made a image which will show in each page with what my site contains
![image](/static/og.png)

Small things that i made sure of:
* my blog boards have spaces in their names, so the page link goes through `urlencode`, which if not present can make link in the tag broken
* added `canonical` so google knows the real address of each page

![alt text](/images/image57.png)

**Change 2:** I added favicon, I designed a favicon in affinity which is basically a heart and a little sparkle
![image](/static/favicon.svg)

It's exported in 3 sizes: `favicon.svg` (basically svg format), `favicon.png` (32x32 for old type browsers) and `apple-touch-icon.png` (180px for when you add to phone's home screen, just in case :D)

**Change 3:** Basically in blog boards page, the post name was being compared as text rather than number which made `devlog-9` be latest even when `devlog-15` was present, it was due to it comparing them as text
![alt text](/images/image58.png)
![alt text](/images/image59.png)

**Change 4:** Originally, when someone visited a directory which doesn't exists, this showed up

![alt text](/images/image60.png)

but lets change it to something cool, shall we???
So I made an animated page, basically its animated like the zero acts as a eye which closes from time to time
![alt text](/images/image61.png)

uhmm, you can look at the frames but idk how to show it thru images
![image](/static/404amn.png)

**How it works:**
* all 4 frams are drawn side by side in one png (a sprite sheet), so the browser only loads one image a time
* the png is used as a mask, which means only its shape matters, not its colour. The color comes from `--text-color`, so its theme changable
* a css animation jumps between the 4 frames with `step-end`, so it snaps from frame to frame instead of sliding
* and if someone turned off animations in their settings, it just stays still

**Change 5:** 