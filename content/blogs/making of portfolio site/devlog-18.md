# changing the color pallet

1) Ermm sooo I wanted to experiment with more colors sooo I decided to test different colors.. like
```css
[data-theme="dark"] {
    --bg-color: #160924;
    --card-bg: #231036;
    --text-color: #b8f28a;
}

[data-theme="light"] {
    --bg-color: #f6faf2;
    --card-bg: #e5f0dc;
    --text-color: #4a156e;
}
```

This
```css
[data-theme="dark"] {
    --bg-color: #06161e;
    --card-bg: #0c232e;
    --text-color: #ffb482;
}

[data-theme="light"] {
    --bg-color: #fdf6f0;
    --card-bg: #f5e6d8;
    --text-color: #0b4f6c;
}
```

also this
```css
:root, [data-theme="dark"] {
    --bg-color: #120d0c;
    --card-bg: #1e1614;
    --text-color: #ffb09e;
}

[data-theme="light"] {
    --bg-color: #f8f5f0;
    --card-bg: #ede7de;
    --text-color: #c4361d;
}
```


and finally the one which I liked isss
```css
:root, [data-theme="dark"] {
    --bg-color: #090624;
    --card-bg: #13113b;
    --text-color: #f2d48d;
}

[data-theme="light"] {
    --bg-color: #f9f6f2;
    --card-bg: #ede7df;
    --text-color: #24195e;
}
```

This kinda gibes the premium and cool like vibess. Where the text pops up and kinda feels intentionalll designn

2) Changing vinyl from song card:

So the vinyl looks abit washed out sooo I decided to change it too.. and I started to play with value, with new styles and everything and at the end what worked was
```css
background:
    /* light reflectionnn */
    conic-gradient(
        from 25deg,
        transparent 0deg,
        rgba(255, 255, 255, 0.16) 28deg,
        rgba(255, 255, 255, 0.03) 55deg,
        transparent 95deg,
        transparent 180deg,
        rgba(255, 255, 255, 0.16) 208deg,
        rgba(255, 255, 255, 0.03) 235deg,
        transparent 275deg
    ),
    
    /* ring and other edgee */
    radial-gradient(
        circle,
        transparent 0% 24%,
        rgba(0, 0, 0, 0.35) 24.5% 33%,
        rgba(255, 255, 255, 0.07) 33.5%,
        transparent 34.5% 96%,
        rgba(0, 0, 0, 0.4) 97% 100% 
    ),
    
    /* grooves thingy (circles running out) */
    repeating-radial-gradient(
        circle,
        rgba(0, 0, 0, 0.28) 0px,
        rgba(0, 0, 0, 0.28) 1px,
        rgba(255, 255, 255, 0.04) 1px,
        rgba(255, 255, 255, 0.04) 3px
    ),

    /* vinyl basee */
    color-mix(in srgb, #080b14 82%, var(--card-bg));
```

and in addition to this, i added:
```css
border: 1px solid color-mix(in srgb, var(--text-color) 22%, transparent);
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.32);
```
for box shadow and border... and noww it looks damn coolll

![alt text](/images/image72.png)

but the issue is the light mode, the text is not clear

![alt text](/images/image73.png)

3) Fixing the vinyl in light theme:

**first attempt:** using `-webkit-text-stroke: 2px var(--bg-color);` i tried making the outer text be the color of background

![alt text](/images/image74.png)

but this didn't give the vibe that i wanted so lets try another approachhh

**another attempt:** 