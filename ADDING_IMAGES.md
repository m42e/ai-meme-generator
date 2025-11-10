# Adding Actual Meme Images

The meme generator works with placeholder images by default, but you can add real meme template images for better results.

## Steps to Add Real Meme Images

1. Create the `memes` directory (already exists):
   ```bash
   mkdir -p memes
   ```

2. Add your meme image files to match the paths in `meme_database.json`:
   - `memes/distracted_boyfriend.jpg`
   - `memes/drake_hotline.jpg`
   - `memes/two_buttons.jpg`
   - `memes/change_my_mind.jpg`
   - `memes/expanding_brain.jpg`
   - `memes/is_this.jpg`
   - `memes/galaxy_brain.jpg`
   - `memes/woman_yelling_at_cat.jpg`
   - `memes/success_kid.jpg`
   - `memes/spiderman_pointing.jpg`

3. The images should be JPEG or PNG format with appropriate dimensions for the text boxes defined in the database.

## Finding Meme Template Images

You can find meme template images from:
- [imgflip.com](https://imgflip.com/memegenerator) - Popular meme generator with templates
- [knowyourmeme.com](https://knowyourmeme.com/) - Meme documentation and templates
- Search for "meme template" + the meme name (e.g., "drake meme template")

**Note**: When using images, ensure you have the right to use them and comply with copyright/licensing requirements.

## Adjusting Text Boxes

If the text boxes don't align well with your images, you can edit `meme_database.json` to adjust:
- `x`, `y`: Top-left position of the text box
- `width`, `height`: Dimensions of the text box
- `align`: Text alignment (`left`, `center`, or `right`)

Example:
```json
{
  "id": "top",
  "x": 350,
  "y": 50,
  "width": 300,
  "height": 150,
  "align": "left"
}
```

## Creating Custom Meme Templates

You can also add your own custom meme templates:

1. Add your meme image to the `memes` directory
2. Add an entry to `meme_database.json`:
   ```json
   {
     "id": "my_custom_meme",
     "name": "My Custom Meme",
     "description": "Detailed description of when to use this meme",
     "image_path": "memes/my_custom_meme.jpg",
     "text_boxes": [
       {
         "id": "top_text",
         "x": 100,
         "y": 50,
         "width": 400,
         "height": 100,
         "align": "center"
       }
     ]
   }
   ```

3. Test it with:
   ```bash
   python meme_generator.py list
   python meme_generator.py generate "your prompt" top_text:"Your text"
   ```
