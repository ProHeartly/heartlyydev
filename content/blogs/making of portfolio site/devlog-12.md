# My projects sectionnn (one of the highlights):

My projects section is one of the main highlight of any personal site and therefore, it should be amazing and in a sense awe-ful with both projects and the way its presented!

**Idea 1**: I was thinking of making something similar to the home page UI, but then it would look repetative and boring. Which might also blend-in with every other personal site.

**Idea 2**: The other idea that I had was something like first idea but instead of two rows, one row will be project and in down there will be a dedicated section for us to view more info about the project.
![alt text](/images/image43.png)

**Idea 3**: What I'm thinking of is like each projects are styled horizontally represented by books, and books are turned like only side of book where little name or art is made is shown (we can keep project names there), and when we click or hover on a book, it turns to its front side and there will be two buttons, demo (if it has) and github.

![alt text](/images/image44.png)


**Verdict**: So I kinda liked the 3rd idea as it is kinda unique and also would be fun for me to make it. Well, let's get goinnn

**Also**: I wanna make projects listed in projects.json inside content so that I dont need to change html everytime I make new project.

# Progress:
1) Making da POC:
Before makign everything using projects.json, i wanted to design the UI and the UX.

**How the books turns**: This was the fun part!! Each book has two faces and we change them like we said:
* the **side** (spine) that faces you, with the project name written sideways using `writing-mode: vertical-rl`
* the **cover**, which is actually sitting *sideways*, sticking out backwards from the spine with `rotateY(90deg)`, just like a real book on a shelf

and also real shelves don't have identical books, so every book gets its own width, height, colour and font using `nth-child(7n + 1)`, `nth-child(7n + 2)`... The pattern repeats every 7 books, so it works no matter how many projects I add.

And I also made some qol if there are too many projects and we have to scroll to rest, as well as made reponsive UI

Bugs I ran into (there were a few...)
* All my books were piled up in the top left corner. I forgot the `.inner` rule, so the faces were positioned against the whole page instead of the book.
* My mixed fonts didn't show up because I renamed `.spine` to `.side` but forgot the font rules.
* Clicking did nothing because I wrote `.books` instead of `.book`, and then used `books` for both the list AND each single book
* `scrollbar-width: 0` doesn't exist, it's `none` (and Safari needs `::-webkit-scrollbar { display: none }` too).
![alt text](/images/image45.png)