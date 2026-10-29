# Mobile friendlyyy, finally!

Sooo, after alot of comments from my friends about the site not being mobile friendly aka responsive, I will be making this mobile responsivee!!

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