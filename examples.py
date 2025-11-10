#!/usr/bin/env python3
"""
Example script showing various ways to use the AI Meme Generator
"""

import os
import sys
from meme_generator import MemeGenerator


def run_examples():
    """Run several example meme generations."""
    
    print("AI Meme Generator - Examples")
    print("=" * 80)
    print()
    
    generator = MemeGenerator()
    
    examples = [
        {
            "name": "Two Buttons Meme",
            "prompt": "choosing between two difficult options",
            "texts": {
                "left_button": "Study for exam",
                "right_button": "Play games",
                "label": "Students"
            },
            "output": "example_two_buttons.jpg"
        },
        {
            "name": "Drake Meme",
            "prompt": "rejecting one thing and approving another",
            "texts": {
                "top": "Using complicated frameworks",
                "bottom": "Using AI tools"
            },
            "output": "example_drake.jpg"
        },
        {
            "name": "Success Kid",
            "prompt": "celebrating a small victory",
            "texts": {
                "top": "Code not working all day",
                "bottom": "Fixed with one line"
            },
            "output": "example_success.jpg"
        },
        {
            "name": "Change My Mind",
            "prompt": "stating a controversial opinion",
            "texts": {
                "sign": "AI will write all code in the future"
            },
            "output": "example_change_mind.jpg"
        },
        {
            "name": "Distracted Boyfriend",
            "prompt": "being distracted by something new",
            "texts": {
                "girlfriend": "Old tech",
                "boyfriend": "Developers",
                "other_woman": "New shiny framework"
            },
            "output": "example_distracted.jpg"
        },
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. Generating: {example['name']}")
        print(f"   Prompt: {example['prompt']}")
        print(f"   Texts: {example['texts']}")
        
        try:
            output_path = generator.generate_meme(
                example['prompt'],
                example['texts'],
                example['output']
            )
            print(f"   ✓ Saved to: {output_path}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print()
    
    print("=" * 80)
    print("All examples generated! Check the output files.")


def interactive_mode():
    """Run the generator in interactive mode."""
    
    print("AI Meme Generator - Interactive Mode")
    print("=" * 80)
    print()
    
    generator = MemeGenerator()
    
    # Show available memes
    generator.list_memes()
    
    print("=" * 80)
    print("Enter your meme idea:")
    prompt = input("Prompt (describe the situation): ")
    
    if not prompt:
        print("No prompt provided, exiting.")
        return
    
    # Find the best meme
    best_meme, score = generator.find_best_meme(prompt)
    
    print(f"\nBest match: {best_meme['name']}")
    print(f"Text boxes needed: {', '.join([box['id'] for box in best_meme['text_boxes']])}")
    print()
    
    # Get text inputs
    text_inputs = {}
    for text_box in best_meme['text_boxes']:
        text = input(f"Text for '{text_box['id']}': ")
        if text:
            text_inputs[text_box['id']] = text
    
    # Generate the meme
    output_path = input("\nOutput filename (default: output_meme.jpg): ") or "output_meme.jpg"
    
    try:
        result = generator.generate_meme(prompt, text_inputs, output_path)
        print(f"\n✓ Success! Meme generated at: {result}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        run_examples()


if __name__ == "__main__":
    main()
