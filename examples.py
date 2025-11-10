#!/usr/bin/env python3
"""
Example script showing various ways to use the AI Meme Generator
"""

import os
import sys
from meme_generator import MemeGenerator


def run_auto_examples():
    """Run examples using the new automatic mode."""
    
    print("AI Meme Generator - Auto Mode Examples")
    print("=" * 80)
    print("Demonstrating the new automatic mode where AI generates all text!\n")
    
    generator = MemeGenerator()
    
    statements = [
        ("Students struggling to decide between studying and playing games", "example_auto_students.jpg"),
        ("I think AI will replace all programmers by 2030", "example_auto_opinion.jpg"),
        ("Developers distracted by new shiny frameworks instead of finishing projects", "example_auto_distracted.jpg"),
        ("Finally fixed that bug that was bothering me for days", "example_auto_success.jpg"),
        ("Should I refactor this code or leave it alone", "example_auto_choice.jpg"),
    ]
    
    for i, (statement, output) in enumerate(statements, 1):
        print(f"{i}. Statement: {statement}")
        
        try:
            output_path = generator.generate_meme_auto(statement, output)
            print(f"   ✓ Saved to: {output_path}\n")
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
    
    print("=" * 80)
    print("Auto-generated examples complete! Check the output files.")


def run_manual_examples():
    """Run examples using manual text specification (original mode)."""
    
    print("\nAI Meme Generator - Manual Mode Examples")
    print("=" * 80)
    print("Demonstrating manual mode with specific text for each box:\n")
    
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
    print("\nChoose mode:")
    print("1. Automatic mode (AI generates all text)")
    print("2. Manual mode (you specify text for each box)")
    mode = input("Enter choice (1 or 2, default: 1): ").strip() or "1"
    
    print("\nEnter your meme idea:")
    statement = input("Statement/situation: ")
    
    if not statement:
        print("No statement provided, exiting.")
        return
    
    output_path = input("Output filename (default: output_meme.jpg): ") or "output_meme.jpg"
    
    try:
        if mode == "1":
            # Automatic mode
            result = generator.generate_meme_auto(statement, output_path)
            print(f"\n✓ Success! Meme generated at: {result}")
        else:
            # Manual mode
            best_meme, score = generator.find_best_meme(statement)
            
            print(f"\nBest match: {best_meme['name']}")
            print(f"Text boxes needed: {', '.join([box['id'] for box in best_meme['text_boxes']])}")
            print()
            
            # Get text inputs
            text_inputs = {}
            for text_box in best_meme['text_boxes']:
                text = input(f"Text for '{text_box['id']}': ")
                if text:
                    text_inputs[text_box['id']] = text
            
            result = generator.generate_meme(statement, text_inputs, output_path)
            print(f"\n✓ Success! Meme generated at: {result}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    elif len(sys.argv) > 1 and sys.argv[1] == "manual":
        run_manual_examples()
    elif len(sys.argv) > 1 and sys.argv[1] == "auto":
        run_auto_examples()
    else:
        # Run both auto and manual examples
        run_auto_examples()
        print("\n\n")
        run_manual_examples()


if __name__ == "__main__":
    main()
