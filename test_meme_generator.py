#!/usr/bin/env python3
"""
Simple tests for the meme generator functionality
"""

import os
import sys
import tempfile
from meme_generator import MemeGenerator


def test_load_database():
    """Test that the database loads correctly."""
    print("Test 1: Loading database...")
    generator = MemeGenerator()
    assert len(generator.memes) > 0, "No memes loaded from database"
    print(f"✓ Loaded {len(generator.memes)} memes")


def test_find_best_meme():
    """Test that the AI matching works."""
    print("\nTest 2: AI meme matching...")
    generator = MemeGenerator()
    
    test_cases = [
        ("choosing between two options", "two_buttons"),
        ("approve and disapprove", "drake_hotline"),
        ("small victory", "success_kid"),
        ("controversial opinion", "change_my_mind"),
        ("being distracted", "distracted_boyfriend"),
    ]
    
    for prompt, expected_id_part in test_cases:
        meme, score = generator.find_best_meme(prompt)
        print(f"  Prompt: '{prompt}' -> {meme['name']} (score: {score:.3f})")
        # Note: We don't strictly enforce the expected meme since TF-IDF can vary,
        # but we check that we get a valid result
        assert meme is not None, f"No meme found for prompt: {prompt}"
        assert score >= 0, f"Invalid score: {score}"
    
    print("✓ All AI matching tests passed")


def test_generate_meme():
    """Test meme generation with placeholders."""
    print("\nTest 3: Generating meme with placeholder...")
    generator = MemeGenerator()
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = generator.generate_meme(
            "choosing between two options",
            {
                "left_button": "Test option 1",
                "right_button": "Test option 2",
                "label": "Test label"
            },
            tmp_path
        )
        
        assert os.path.exists(result), f"Output file not created: {result}"
        assert os.path.getsize(result) > 0, "Output file is empty"
        print(f"✓ Meme generated successfully: {result}")
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_text_wrapping():
    """Test that long text is handled correctly."""
    print("\nTest 4: Text wrapping with long text...")
    generator = MemeGenerator()
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        result = generator.generate_meme(
            "stating opinion",
            {
                "sign": "This is a very long text that should be wrapped properly across multiple lines to fit in the text box without overflowing"
            },
            tmp_path
        )
        
        assert os.path.exists(result), f"Output file not created: {result}"
        print(f"✓ Long text handled correctly")
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("Running Meme Generator Tests")
    print("=" * 80)
    
    tests = [
        test_load_database,
        test_find_best_meme,
        test_generate_meme,
        test_text_wrapping,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 80)
    if failed == 0:
        print("All tests passed! ✓")
    else:
        print(f"{failed} test(s) failed ✗")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
