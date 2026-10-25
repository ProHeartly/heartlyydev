# Returned with more ideasszzz

Sooo, I went on a short vacation without my laptop, therefore, I couldn't work on anything but in mean time, I did think of ideaszzzz.

### Ideaszzz:
* Improving da animation: Sooo the animation currently is cool but I thought of something cooler, LIKE I want the cards which are in down row to appear from down like fly-in (from ppt) but smoothhhherr.
* About page: I finally got kinda idea for about me page, I'm thinking of something like newspaper styled site. (smth like the new york times ish).
* (MAYBE) making a gallery upload section, where it requires a code and allows me to upload image and caption from the web..
* A mail system might be a coolllllll idea but idk how to make it soo i consider this as a far-fetched idea


## Progress:
1) Made animation that I was thinking of:
    ![gif](/images/animation.gif)
    this was done by adding `transform: translateY(140px);` to `.card`. But I remembered, I want two types of animation (from up and down), so i added 
    ```
    .row:first-child .card:not(.in-view) {
    transform: translateY(-140px);
    }
    ```
    this makes the top thingy move `-140px` (up).

2) Made the about me pageee:
![alt text](/images/image13.png)
This is the current look of about me page and ofc it also has the theme change :)

![alt text](/images/image14.png)