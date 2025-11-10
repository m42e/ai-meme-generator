#!/usr/bin/env python3
"""
AI Meme Generator

This script generates memes by:
1. Loading a database of meme templates with descriptions
2. Using AI (Mistral AI) to find the best meme for a user's prompt
3. Overlaying text on the selected meme image
4. Saving the generated meme
"""

import json
import os
import sys
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from mistralai import Mistral


class MemeGenerator:
    """Main class for AI-powered meme generation."""
    
    def __init__(self, database_path: str = "meme_database.json", api_key: Optional[str] = None):
        """
        Initialize the meme generator.
        
        Args:
            database_path: Path to the JSON file containing meme templates
            api_key: Mistral API key (if not provided, will look for MISTRAL_API_KEY env var)
        """
        self.database_path = database_path
        self.memes = self._load_database()
        
        # Initialize Mistral client
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            print("Warning: No Mistral API key found. Set MISTRAL_API_KEY environment variable.")
            print("Falling back to simple keyword matching.")
            self.client = None
        else:
            self.client = Mistral(api_key=self.api_key)
            print("Initialized Mistral AI client")
    
    def _load_database(self) -> List[Dict]:
        """Load the meme database from JSON file."""
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(f"Meme database not found at {self.database_path}")
        
        with open(self.database_path, 'r') as f:
            memes = json.load(f)
        
        print(f"Loaded {len(memes)} meme templates from database")
        return memes
    
    def find_best_meme(self, user_prompt: str) -> Tuple[Dict, float]:
        """
        Find the best matching meme for the user's prompt using Mistral AI.
        
        Args:
            user_prompt: The user's text/prompt describing what they want
            
        Returns:
            Tuple of (best_meme_dict, similarity_score)
        """
        if self.client:
            return self._find_best_meme_with_mistral(user_prompt)
        else:
            return self._find_best_meme_fallback(user_prompt)
    
    def _find_best_meme_with_mistral(self, user_prompt: str) -> Tuple[Dict, float]:
        """Use Mistral AI to find the best meme."""
        # Create a prompt for Mistral to analyze which meme fits best
        meme_options = []
        for i, meme in enumerate(self.memes):
            meme_options.append(f"{i+1}. {meme['name']}: {meme['description']}")
        
        meme_list = "\n".join(meme_options)
        
        system_prompt = """You are a meme selection expert. Given a user's statement or situation, 
you need to select the most appropriate meme template from the provided list. 
Respond with ONLY the number of the best matching meme (1-10) and a confidence score (0.0-1.0) 
in the format: "NUMBER SCORE". For example: "3 0.85" """
        
        user_message = f"""User's statement: "{user_prompt}"

Available meme templates:
{meme_list}

Which meme template number (1-{len(self.memes)}) best fits this statement? Respond with just the number and confidence score."""

        try:
            # Call Mistral AI
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            # Parse response
            answer = response.choices[0].message.content.strip()
            parts = answer.split()
            
            if len(parts) >= 1:
                meme_number = int(parts[0])
                confidence = float(parts[1]) if len(parts) >= 2 else 0.8
                
                # Validate meme number
                if 1 <= meme_number <= len(self.memes):
                    best_meme = self.memes[meme_number - 1]
                    print(f"Selected meme: '{best_meme['name']}' (confidence: {confidence:.3f})")
                    return best_meme, confidence
            
            # If parsing failed, fall back
            print("Failed to parse Mistral response, using fallback")
            return self._find_best_meme_fallback(user_prompt)
            
        except Exception as e:
            print(f"Mistral AI error: {e}, using fallback")
            return self._find_best_meme_fallback(user_prompt)
    
    def _find_best_meme_fallback(self, user_prompt: str) -> Tuple[Dict, float]:
        """Simple keyword-based fallback matching."""
        prompt_lower = user_prompt.lower()
        best_score = 0.0
        best_meme = self.memes[0]
        
        for meme in self.memes:
            score = 0.0
            description_lower = (meme['description'] + " " + meme['name']).lower()
            
            # Simple keyword matching
            words = prompt_lower.split()
            for word in words:
                if len(word) > 3 and word in description_lower:
                    score += 1.0
            
            # Normalize by number of words
            if words:
                score = score / len(words)
            
            if score > best_score:
                best_score = score
                best_meme = meme
        
        print(f"Selected meme: '{best_meme['name']}' (fallback score: {best_score:.3f})")
        return best_meme, best_score
    
    def generate_text_for_meme(self, user_statement: str, meme: Dict) -> Dict[str, str]:
        """
        Generate text for all text boxes in a meme based on user's statement.
        
        Args:
            user_statement: The user's statement/situation
            meme: The meme template dictionary
            
        Returns:
            Dictionary mapping text box IDs to generated text
        """
        if self.client:
            return self._generate_text_with_mistral(user_statement, meme)
        else:
            return self._generate_text_fallback(user_statement, meme)
    
    def _generate_text_with_mistral(self, user_statement: str, meme: Dict) -> Dict[str, str]:
        """Use Mistral AI to generate text for meme text boxes."""
        # Build description of text boxes
        text_box_descriptions = []
        for box in meme['text_boxes']:
            text_box_descriptions.append(f"- {box['id']}: (text field)")
        
        text_boxes_info = "\n".join(text_box_descriptions)
        text_box_ids = [box['id'] for box in meme['text_boxes']]
        
        system_prompt = """You are a meme text generator. Given a user's statement and a meme template, 
generate appropriate, funny, and relevant text for each text box in the meme.
Keep text short and punchy - memes work best with concise text.
Respond with ONLY a JSON object mapping text box IDs to their text content.
Example format: {"box1": "text for box 1", "box2": "text for box 2"}"""
        
        user_message = f"""User's statement: "{user_statement}"

Meme template: {meme['name']}
Description: {meme['description']}

Text boxes to fill:
{text_boxes_info}

Generate appropriate text for each text box (IDs: {', '.join(text_box_ids)}).
Respond with ONLY valid JSON mapping IDs to text."""

        try:
            # Call Mistral AI
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            # Parse response
            answer = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response
            # Sometimes AI wraps JSON in markdown code blocks
            if "```json" in answer:
                answer = answer.split("```json")[1].split("```")[0].strip()
            elif "```" in answer:
                answer = answer.split("```")[1].split("```")[0].strip()
            
            text_inputs = json.loads(answer)
            
            # Validate that we got text for the expected boxes
            valid_inputs = {}
            for box_id in text_box_ids:
                if box_id in text_inputs:
                    valid_inputs[box_id] = text_inputs[box_id]
            
            if valid_inputs:
                print(f"Generated text for {len(valid_inputs)} text boxes")
                return valid_inputs
            else:
                print("No valid text boxes in Mistral response, using fallback")
                return self._generate_text_fallback(user_statement, meme)
            
        except Exception as e:
            print(f"Mistral AI error in text generation: {e}, using fallback")
            return self._generate_text_fallback(user_statement, meme)
    
    def _generate_text_fallback(self, user_statement: str, meme: Dict) -> Dict[str, str]:
        """Simple fallback text generation."""
        text_inputs = {}
        
        # For simple memes, just split the statement
        words = user_statement.split()
        
        # Different strategies for different meme types
        if meme['id'] == 'drake_hotline':
            # Split into rejection and approval
            mid = len(words) // 2
            text_inputs['top'] = ' '.join(words[:mid]) if mid > 0 else user_statement
            text_inputs['bottom'] = ' '.join(words[mid:]) if mid < len(words) else user_statement
        
        elif meme['id'] == 'two_buttons':
            # Split into two options and label
            third = len(words) // 3
            text_inputs['left_button'] = ' '.join(words[:third]) if third > 0 else "Option 1"
            text_inputs['right_button'] = ' '.join(words[third:2*third]) if third > 0 else "Option 2"
            text_inputs['label'] = ' '.join(words[2*third:]) if 2*third < len(words) else "Person"
        
        elif meme['id'] == 'success_kid':
            # Top and bottom
            mid = len(words) // 2
            text_inputs['top'] = ' '.join(words[:mid]) if mid > 0 else user_statement
            text_inputs['bottom'] = ' '.join(words[mid:]) if mid < len(words) else "Success!"
        
        else:
            # Generic: use the statement for the first text box
            if meme['text_boxes']:
                text_inputs[meme['text_boxes'][0]['id']] = user_statement
        
        print(f"Generated fallback text for {len(text_inputs)} text boxes")
        return text_inputs
    
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
    
    def generate_meme_auto(self, user_statement: str, 
                           output_path: str = "output_meme.jpg",
                           create_placeholder: bool = True) -> str:
        """
        Automatically generate a complete meme from just a user statement.
        
        This method:
        1. Selects the best meme template based on the statement
        2. Generates appropriate text for all text boxes
        3. Creates and saves the meme
        
        Args:
            user_statement: The user's statement or situation
            output_path: Where to save the generated meme
            create_placeholder: If True and image doesn't exist, create a placeholder
            
        Returns:
            Path to the generated meme
        """
        print(f"\nGenerating meme from statement: '{user_statement}'")
        
        # Step 1: Find the best matching meme
        best_meme, score = self.find_best_meme(user_statement)
        
        # Step 2: Generate text for all text boxes
        text_inputs = self.generate_text_for_meme(user_statement, best_meme)
        
        print(f"\nGenerated text:")
        for box_id, text in text_inputs.items():
            print(f"  {box_id}: '{text}'")
        
        # Step 3: Generate the meme
        return self.generate_meme(user_statement, text_inputs, output_path, create_placeholder)
    
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
        print("\n  python meme_generator.py generate <statement>")
        print("    - Automatically generate a complete meme from your statement")
        print("    - AI selects template AND generates all text")
        print("\n  python meme_generator.py generate <prompt> [text_box_id:text ...]")
        print("    - Generate a meme with manual text inputs (advanced mode)")
        print("\nExamples:")
        print('  python meme_generator.py generate "Students struggling to choose between studying and playing games"')
        print()
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
            print("Error: Please provide a statement or prompt for meme generation")
            return
        
        statement = sys.argv[2]
        
        # Parse text inputs from remaining arguments
        text_inputs = {}
        for arg in sys.argv[3:]:
            if ':' in arg:
                key, value = arg.split(':', 1)
                text_inputs[key] = value
        
        # Determine mode: auto (no text inputs) or manual (with text inputs)
        output_path = "output_meme.jpg"
        
        try:
            if text_inputs:
                # Manual mode: user provided text for specific boxes
                result = generator.generate_meme(statement, text_inputs, output_path)
            else:
                # Auto mode: AI generates everything
                result = generator.generate_meme_auto(statement, output_path)
            
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
