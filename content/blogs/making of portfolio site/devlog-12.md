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

2) Working with `projects.json`: Instead of writing every book by hand in the HTML, the shelf now builds itself from a `projects.json` file, same idea as how my gallery (`caption.json`) and blogs (markdown folders) work.

Each project is just a little block in the json:
```json
{
    "name": "heartlyy dev",
    "description": "My personal site which is self-hosted, build with fastapi, and with ALOT of care!",
    "picture": "/images/image42.png",
    "demo": "https://heartlyy.dev",
    "github": "https://github.com/ProHeartly/heartlyydev"
}
```

The `/projects` route in `main.py` reads this filee and hands it to the template, and in `projects.html` a `{% for p in projects %}` loop makes one book for each project. So the HTML went from 12 copyy pasted books to just ONE book that repeatsz

Some small things I made sure of:
- `picture` and `demo` are optional. If they're empty (`""`), the book just has no picture or no Demo button instead of a broken one.
- The order in the json = the order on the shelf, so I can rearrange my books by moving the blocks around.
- The file is read every time someone opens the page, so after editing it I just refresh, no restarting the server.
- I added a `.cover img` rule, because without it a big picture would spill out of the cover.


![alt text](/images/image46.png)