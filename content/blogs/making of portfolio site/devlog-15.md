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

