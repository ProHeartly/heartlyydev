# Redesigning my personal site!

![previous](/images/Screenshot%202026-10-16%20123407.png)

This is how, my current personal site looks! Although it looks cool, and I like it's vibes but I think we neeed a redesign.

![rough sketch](/images/image.png)
So this is kinda like rough sketch of my vision. What I'm thinking is, it should have horizontal scrolling, card like design like we had previously but 2 columns, everything smoothly animated, card with kinda soft glowing edges (if it looks good), and most importantly, changes light to dark theme like previous.

## Progress
* ### First progress:
    ![p1](/images/image1.png)
    This is how its looking..

    I kept little variations in the width of cards to `40vw (small ones), 80vw (big ones) and 60vw (transition ones)`. Transition ones are there to help the layout look deliberate typa.

* ### Made underline:
    ![alt text](/images/image2.png)
    I made this cutie underline effect on hover after a long trial and error for value of offset ;-;
    `text-decoration-thickness: 0.5rem;
    text-underline-offset: 0.7rem;`

* ### Lets make animation now:
    I made animation that plays when first time loading that card, it flyIn from down with smooth cubic bezier function `cubic-bezier(0.16, 1, 0.3, 1)`, this makes the animation really smooth.

* ### Vertical scroll converted to horizontal scroll:
    basically now when you normally scroll, the `scroll.js` captures it, and converts that into `container.scrollLeft += e.deltaY ;` the container scrolling horizontally.
    And i also fixed a minor spelling mistake: turns our I spelled `observer` as `obserber` in `animation.js`.

    But still, the scrolling thing looks choppy, so I might add the accelerated scrolling effect.

* ### I made da scrolling accelerated:
    So how this works is; `velocity += e.deltaY * 0.18;` this provides the momentum build-up which means if its scrolling then it builds up the momentum and `velocity *= 0.92;` this line inside the `Animate` function acts as damping or friction to eventually stop the velocity. Here, I experimented with different values of them and found `0.92` for friction and `0.18` for momentum as good!