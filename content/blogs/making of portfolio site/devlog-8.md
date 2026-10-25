# blogszz finally
Finally added blogzz

I'm thinking of design smth like this:
![alt text](/images/blog.png)
Like each blog pages are inside folder type with a label so we can manage them properly.

* So, my idea: blog thingy also like gallery (generates from whats in the storage) and in a more organized manner. Lets say blogs are stored inside `/content/blogs` and each folder is considered a board, meaning a title type and inside those folders are blog pages so for eg: a folder -> portfolio devlog, inside -> devlog-1, devlog-2, etc. And in site too, we show in a similar way, we use `<i class="ph-duotone ph-folder"></i>` to denote the folder and names of the title which are just folder name, then when user clicks a folder, all the pages (stored in .md) are shown with title as their name. Each page will be in theme of newspaper :)

* Another idea: instead of making new page for each one, I will be making a `blog_base.html` which will have the boilerplate and each site will be developed below that

# Progress:
1) I'm almost done with baseplate: So erm to simply stuff, the colorpallet will be transformation of the whats alr there in `style.css` and I'm thinking of using one single `blog.css` for the css.(by this i mean all the css will be stored in same place to remove too many css files T_T). Also the theme of the site as I said, wil be kinda inspired from newszz so
![alt text](/images/image19.png)

2) Done with board styled page where all the main blogs are displayed
![alt text](/images/image20.png)

3) I finished the boards pages:
![alt text](/images/image21.png)
basically, this is the collection of pages which are in the folder :D

4) Sooo the pages of blog is also completed
![alt text](/images/image22.png)
Uhh from here I see styling is left and the images are not loading soo I will be searching how to load images later and in mean time, making the styling :)