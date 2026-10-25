# Making gallery:

Btw I was at first trying to make about me but ran out of idea so for now this is what about me looks like
![alt text](/images/image10.png)

I will work on it when I get some idea for it!

Beside that, lets work on galleryy! I wana make smth like [this](https://proheartly.github.io/my-gallery/) with custom font and all :D

**forgot to mention!**
I hosted this in nest thingy, it took me a while, **A WHILE** to host it but finally its hosted in [this](https://heartly.dev) (and yahhhh I used my custom domain :D)

**Made the gallery!**
![alt text](/images/image11.png)

Also! now it auto updates if I put any image inside `/content/gallery` but I do need to put captions in `/content/caption.json` with format `"<image_name>.<image_extension>": "<caption>"`. This was done using
```
def gallery(request: Request):
    images = []
    captions = {}
    captions = json.loads(caption_path.read_text(encoding="utf-8"))
    for f in sorted(gallery_path.iterdir()):
        images.append({
            "file": f.name,
            "caption": captions.get(f.name, f.stem),
        })

    return src.TemplateResponse(
        request=request,
        name="gallery.html",
        context={"request": request, "images": images},
    )
```
Here, it iterates thru the folder `/content/gallery` and adds that to `images` along with it caption from `captions` and sends it to the html by `context={"request": request, "images": images}`. Although `"request": request"` is not necessay, I was getting error prevoiusly so I placed it just in case.

This request gets picked up by `gallery.html`
and using:
```
<div class="photos">
    {% for img in images %}
    <div class="photo">
        <img src="{{ url_for('gallery', path=img.file) }}" alt="{{ img.caption }}">
        <p>{{ img.caption }}</p>
    </div>
    {% endfor %}
</div>
```
it creates the automatic gallery thingy :)

**small qol:**
![alt text](/images/image12.png)

Erm there was no context to what the song was soo, I added a little what it is, which also disappears when I'm not listening to anything.
