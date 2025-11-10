#!/usr/bin/env python3
"""
AI Meme Generator

This script generates memes by:
1. Loading a database of meme templates with descriptions
2. Using AI (TF-IDF semantic matching) to find the best meme for a user's prompt
3. Overlaying text on the selected meme image
4. Saving the generated meme
"""

import json
import os
import sys
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MemeGenerator:
    """Main class for AI-powered meme generation."""
    
    def __init__(self, database_path: str = "meme_database.json"):
        """
        Initialize the meme generator.
        
        Args:
            database_path: Path to the JSON file containing meme templates
        """
        self.database_path = database_path
        self.memes = self._load_database()
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self._precompute_embeddings()
    
    def _load_database(self) -> List[Dict]:
        """Load the meme database from JSON file."""
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(f"Meme database not found at {self.database_path}")
        
        with open(self.database_path, 'r') as f:
            memes = json.load(f)
        
        print(f"Loaded {len(memes)} meme templates from database")
        return memes
    
    def _precompute_embeddings(self):
        """Precompute TF-IDF vectors for all meme descriptions."""
        descriptions = [meme['description'] + " " + meme['name'] for meme in self.memes]
        self.meme_vectors = self.vectorizer.fit_transform(descriptions)
        print("Precomputed TF-IDF vectors for all meme templates")
    
    def find_best_meme(self, user_prompt: str) -> Tuple[Dict, float]:
        """
        Find the best matching meme for the user's prompt using semantic similarity.
        
        Args:
            user_prompt: The user's text/prompt describing what they want
            
        Returns:
            Tuple of (best_meme_dict, similarity_score)
        """
        # Vectorize the user prompt
        prompt_vector = self.vectorizer.transform([user_prompt])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(prompt_vector, self.meme_vectors)[0]
        
        # Find the best match
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        
        best_meme = self.memes[best_idx]
        print(f"Selected meme: '{best_meme['name']}' (similarity: {best_score:.3f})")
        
        return best_meme, best_score
    
    def _get_font(self, size: int = 40) -> ImageFont.FreeTypeFont:
        """
        Get a font for text rendering.
        
        Args:
            size: Font size
            
        Returns:
            ImageFont object
        """
        # Try to use Impact font (classic meme font) or fall back to default
        font_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Windows/Fonts/impact.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    pass
        
        # Fall back to default font
        return ImageFont.load_default()
    
    def _draw_text_with_outline(self, draw: ImageDraw.Draw, text: str, 
                                 x: int, y: int, width: int, height: int,
                                 align: str = "center", font_size: int = 40):
        """
        Draw text with a black outline for visibility.
        
        Args:
            draw: ImageDraw object
            text: Text to draw
            x, y: Top-left position of text box
            width, height: Dimensions of text box
            align: Text alignment ('left', 'center', 'right')
            font_size: Font size
        """
        font = self._get_font(font_size)
        
        # Word wrap text to fit in box
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= width - 20:  # 20px padding
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate starting y position to center text vertically
        bbox = draw.textbbox((0, 0), "Ay", font=font)
        line_height = bbox[3] - bbox[1] + 5
        total_height = line_height * len(lines)
        start_y = y + (height - total_height) // 2
        
        # Draw each line
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            
            # Calculate x position based on alignment
            if align == "center":
                text_x = x + (width - text_width) // 2
            elif align == "right":
                text_x = x + width - text_width - 10
            else:  # left
                text_x = x + 10
            
            text_y = start_y + i * line_height
            
            # Draw outline (black)
            for offset_x in [-2, -1, 0, 1, 2]:
                for offset_y in [-2, -1, 0, 1, 2]:
                    if offset_x != 0 or offset_y != 0:
                        draw.text((text_x + offset_x, text_y + offset_y), 
                                  line, font=font, fill="black")
            
            # Draw text (white)
            draw.text((text_x, text_y), line, font=font, fill="white")
    
    def generate_meme(self, user_prompt: str, text_inputs: Dict[str, str],
                      output_path: str = "output_meme.jpg",
                      create_placeholder: bool = True) -> str:
        """
        Generate a meme based on user prompt and text inputs.
        
        Args:
            user_prompt: Description of the meme situation
            text_inputs: Dictionary mapping text box IDs to text content
            output_path: Where to save the generated meme
            create_placeholder: If True and image doesn't exist, create a placeholder
            
        Returns:
            Path to the generated meme
        """
        # Find the best matching meme
        best_meme, score = self.find_best_meme(user_prompt)
        
        # Load or create the base image
        image_path = best_meme['image_path']
        
        if not os.path.exists(image_path):
            if create_placeholder:
                print(f"Image not found: {image_path}, creating placeholder")
                img = self._create_placeholder_image(best_meme)
            else:
                raise FileNotFoundError(f"Meme image not found: {image_path}")
        else:
            img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Add text to each text box
        for text_box in best_meme['text_boxes']:
            box_id = text_box['id']
            if box_id in text_inputs and text_inputs[box_id]:
                self._draw_text_with_outline(
                    draw,
                    text_inputs[box_id],
                    text_box['x'],
                    text_box['y'],
                    text_box['width'],
                    text_box['height'],
                    text_box.get('align', 'center')
                )
        
        # Save the generated meme
        img.save(output_path, quality=95)
        print(f"Meme saved to: {output_path}")
        
        return output_path
    
    def _create_placeholder_image(self, meme: Dict) -> Image.Image:
        """
        Create a placeholder image for a meme template.
        
        Args:
            meme: Meme template dictionary
            
        Returns:
            PIL Image object
        """
        # Calculate image size based on text boxes
        max_x = max(box['x'] + box['width'] for box in meme['text_boxes'])
        max_y = max(box['y'] + box['height'] for box in meme['text_boxes'])
        
        width = max(600, max_x + 50)
        height = max(500, max_y + 50)
        
        # Create a simple gradient background
        img = Image.new('RGB', (width, height), color='lightgray')
        draw = ImageDraw.Draw(img)
        
        # Add title
        font = self._get_font(30)
        title = f"Placeholder: {meme['name']}"
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((width // 2 - text_width // 2, 20), title, font=font, fill="black")
        
        # Draw text box boundaries
        for text_box in meme['text_boxes']:
            x, y = text_box['x'], text_box['y']
            w, h = text_box['width'], text_box['height']
            draw.rectangle([x, y, x + w, y + h], outline="blue", width=2)
            
            # Draw text box label
            small_font = self._get_font(20)
            draw.text((x + 5, y + 5), text_box['id'], font=small_font, fill="darkblue")
        
        return img
    
    def list_memes(self):
        """Print a list of available meme templates."""
        print("\nAvailable Meme Templates:")
        print("=" * 80)
        for i, meme in enumerate(self.memes, 1):
            print(f"{i}. {meme['name']} ({meme['id']})")
            print(f"   Description: {meme['description'][:100]}...")
            print(f"   Text boxes: {', '.join([box['id'] for box in meme['text_boxes']])}")
            print()


def main():
    """Main function to run the meme generator."""
    if len(sys.argv) < 2:
        print("AI Meme Generator")
        print("=" * 80)
        print("\nUsage:")
        print("  python meme_generator.py list")
        print("    - List all available meme templates")
        print("\n  python meme_generator.py generate <prompt> [text_box_id:text ...]")
        print("    - Generate a meme based on prompt and text inputs")
        print("\nExample:")
        print('  python meme_generator.py generate "choosing between two options" \\')
        print('    left_button:"Do homework" right_button:"Play games" label:"Students"')
        print()
        return
    
    command = sys.argv[1]
    generator = MemeGenerator()
    
    if command == "list":
        generator.list_memes()
    
    elif command == "generate":
        if len(sys.argv) < 3:
            print("Error: Please provide a prompt for meme generation")
            return
        
        prompt = sys.argv[2]
        
        # Parse text inputs from remaining arguments
        text_inputs = {}
        for arg in sys.argv[3:]:
            if ':' in arg:
                key, value = arg.split(':', 1)
                text_inputs[key] = value
        
        # Generate the meme
        output_path = "output_meme.jpg"
        try:
            result = generator.generate_meme(prompt, text_inputs, output_path)
            print(f"\n✓ Success! Meme generated at: {result}")
        except Exception as e:
            print(f"\n✗ Error generating meme: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'list' or 'generate'")


if __name__ == "__main__":
    main()
