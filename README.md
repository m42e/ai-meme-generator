# AI Meme Generator

An intelligent meme generator that uses AI to automatically select the perfect meme template and generate text based on your statement. Just describe your situation, and let the AI do the rest!

## Features

- 🎯 **Fully Automatic Mode**: Just provide a statement - AI selects the meme AND generates all text!
- 🤖 **AI-Powered Selection**: Uses Mistral AI to intelligently match your statement to the best meme template
- ✍️ **AI Text Generation**: Automatically generates appropriate, funny text for all meme text boxes
- 📝 **Smart Text Overlay**: Automatically positions text with proper formatting and outlines for readability
- 🎨 **Placeholder Generation**: Creates placeholder images if actual meme templates aren't available
- 💾 **Extensible Database**: Easy-to-modify JSON database of meme templates with descriptions and text box positions
- 🚀 **Simple CLI**: Easy-to-use command-line interface
- 🔄 **Fallback Mode**: Works without API key using keyword matching and basic text generation
- 🎛️ **Manual Mode**: Advanced users can still specify text for each box manually

## How It Works

### Automatic Mode (Recommended)

1. **User provides a statement**: Just describe your situation or idea
2. **AI selects meme template**: Mistral AI analyzes your statement and picks the best meme
3. **AI generates text**: Automatically creates appropriate text for each text box
4. **Creates the meme**: Overlays the generated text and saves your meme

### Manual Mode (Advanced)

1. **Loads meme database**: Reads from `meme_database.json` containing meme templates with:
   - Template descriptions for AI matching
   - Image paths
   - Bounding boxes for text placement
   
2. **AI-powered matching**: Uses Mistral AI to analyze your prompt and intelligently select the most appropriate meme template

3. **Text overlay**: Places your specified text on the meme at predefined locations with proper formatting

4. **Saves result**: Outputs the generated meme as an image file

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/m42e/ai-meme-generator.git
cd ai-meme-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Mistral API key (optional, but recommended for best results):
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

You can get a Mistral API key from [https://console.mistral.ai/](https://console.mistral.ai/)

**Note**: The generator will work without an API key using a simple keyword matching fallback, but Mistral AI provides much better meme selection.

## Usage

### Quick Start - Run Examples

To quickly see the meme generator in action:

```bash
python examples.py
```

This will generate several example memes demonstrating different templates.

For interactive mode:

```bash
python examples.py interactive
```

### List Available Memes

To see all available meme templates:

```bash
python meme_generator.py list
```

This will show you:
- Meme names and IDs
- Descriptions of when to use each meme
- Available text box IDs for each template

### Generate a Meme

#### Automatic Mode (Recommended) - Just Provide a Statement

The easiest way to generate a meme is to simply provide your statement or situation. The AI will:
1. Select the most appropriate meme template
2. Automatically generate text for all text boxes

**Basic syntax:**

```bash
python meme_generator.py generate "<your statement>"
```

**Examples:**

```bash
python meme_generator.py generate "Students struggling to decide between studying and playing games"
```

```bash
python meme_generator.py generate "I believe AI will replace all programmers by 2030"
```

```bash
python meme_generator.py generate "Developers distracted by new shiny frameworks"
```

The AI will analyze your statement, choose the best meme template (like Two Buttons, Change My Mind, or Distracted Boyfriend), and generate appropriate text for each part of the meme.

#### Manual Mode (Advanced) - Specify Text for Each Box

For more control, you can manually specify the text for each text box:

**Basic syntax:**

```bash
python meme_generator.py generate "<your prompt>" [text_box_id:text ...]
```

**Examples:**

**Drake Hotline Bling** - Showing preference:
```bash
python meme_generator.py generate "preferring one thing over another" \
  top:"Using complicated tools" \
  bottom:"Using AI Meme Generator"
```

**Two Buttons** - Difficult choice:
```bash
python meme_generator.py generate "difficult decision between two options" \
  left_button:"Write code manually" \
  right_button:"Use AI assistant" \
  label:"Programmers"
```

**Change My Mind** - Controversial opinion:
```bash
python meme_generator.py generate "stating an opinion to defend" \
  sign:"Python is the best programming language"
```

**Distracted Boyfriend** - Preference for new thing:
```bash
python meme_generator.py generate "being distracted by something new" \
  girlfriend:"Old framework" \
  boyfriend:"Developers" \
  other_woman:"New shiny framework"
```

**Success Kid** - Small victory:
```bash
python meme_generator.py generate "small accomplishment or victory" \
  top:"Tests were failing all morning" \
  bottom:"Fixed it with one line"
```

## Meme Database

The `meme_database.json` file contains all meme templates. Each template includes:

```json
{
  "id": "unique_identifier",
  "name": "Meme Name",
  "description": "Detailed description of when and how to use this meme",
  "image_path": "path/to/image.jpg",
  "text_boxes": [
    {
      "id": "box_identifier",
      "x": 100,
      "y": 50,
      "width": 300,
      "height": 150,
      "align": "center"
    }
  ]
}
```

### Adding Your Own Memes

1. Add your meme image to the `memes/` directory
2. Add an entry to `meme_database.json` with:
   - A clear description for AI matching
   - The image path
   - Text box coordinates and dimensions
3. Test it with `python meme_generator.py list`

## Technical Details

### AI Matching

The generator uses **Mistral AI** for intelligent meme selection:

1. **With API Key**: Sends your prompt and all meme descriptions to Mistral AI's `mistral-small-latest` model
   - The AI analyzes the context and meaning of your prompt
   - Compares it against all available meme templates
   - Returns the best match with a confidence score
   - Provides superior understanding of nuance and context

2. **Fallback Mode** (no API key): Uses simple keyword matching
   - Matches words from your prompt against meme descriptions
   - Works offline without any API requirements
   - Good for basic use cases

### AI Text Generation

The generator uses **Mistral AI** to automatically generate meme text:

1. **With API Key**: Sends your statement, selected meme info, and text box IDs to Mistral AI
   - The AI understands the meme format and your statement
   - Generates appropriate, funny, and contextually relevant text for each box
   - Returns text in the correct format for the meme
   - Keeps text concise and punchy for maximum meme impact

2. **Fallback Mode** (no API key): Uses simple text splitting strategies
   - Different strategies for different meme types (e.g., splits statement in half for Drake meme)
   - Works offline without any API requirements
   - Provides basic but functional text generation

### Text Rendering

- Uses bold system fonts (Liberation Sans, DejaVu, etc.)
- Adds black outlines for text visibility
- Automatically wraps text to fit in bounding boxes
- Centers text vertically and horizontally based on alignment settings

## Dependencies

- **Pillow**: Image manipulation and text rendering
- **mistralai**: Mistral AI client for intelligent meme selection and text generation
- **numpy**: Numerical operations

## Output

Generated memes are saved as `output_meme.jpg` by default. You can specify a different output path in the code if needed.

## Limitations & Future Improvements

Current limitations:
- Requires predefined text box positions for each meme
- Uses placeholder images if actual meme images aren't provided
- Font selection is system-dependent
- Text generation quality improves significantly with Mistral API key

Possible improvements:
- Automatic text box detection using computer vision
- Integration with meme image APIs
- Support for animated GIFs
- Web interface
- More sophisticated text formatting options
- Multi-language support

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to:
- Add new meme templates to the database
- Improve the AI matching algorithm
- Enhance text rendering
- Add new features

## Troubleshooting

**"Meme image not found" error**: The generator will create placeholder images automatically. To use actual meme images, add them to the `memes/` directory with filenames matching the database.

**Text doesn't fit**: Adjust the text box dimensions in `meme_database.json` or shorten your text.

**Poor meme selection**: Try rephrasing your prompt to better match the meme descriptions in the database.

## Examples Gallery

Run the examples above to see the AI in action! The generator will automatically select appropriate memes based on your descriptions.