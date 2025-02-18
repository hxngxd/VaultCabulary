#!/usr/bin/env python3
import os
import random
import re
import keyboard  # For detecting arrow key presses

def parse_markdown_file(filepath):
    """Parses a markdown file and extracts the word and its definition blocks."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the word (first line starting with "# ")
    word_match = re.search(r'^#\s*(.+)', content, re.MULTILINE)
    if not word_match:
        return None
    word = word_match.group(1).strip()
    
    # Split content into blocks using "---" as the separator
    blocks = re.split(r'\n---\n', content)
    
    # Extract definition blocks that contain relevant keywords
    defs = [block.strip() for block in blocks if re.search(r'(Examples:|Synonyms:|Antonyms:)', block)]
    
    return word, defs if defs else None  # Only return if definitions exist

def load_vocabularies(folder):
    """Loads all .md files in the folder and extracts vocabulary words and definitions."""
    vocab_dict = {}  # Store words and their definitions
    for filename in os.listdir(folder):
        if filename.endswith('.md'):
            filepath = os.path.join(folder, filename)
            parsed = parse_markdown_file(filepath)
            if parsed:
                word, defs = parsed
                if defs:
                    vocab_dict[word] = defs[:]  # Make a copy of definitions
    return vocab_dict

def review_vocabularies(vocab_dict):
    """Displays each word with a random definition in cycles until all have been shown."""
    words = list(vocab_dict.keys())  # Get all words
    random.shuffle(words)  # Shuffle word order

    word_def_tracker = {word: random.sample(defs, len(defs)) for word, defs in vocab_dict.items()}  # Shuffle definitions
    
    review_list = []  # Flatten words with each definition into a review list
    for word in words:
        for definition in word_def_tracker[word]:
            review_list.append((word, definition))

    index = 0  # Track current position in the review list
    
    while index < len(review_list):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        
        word, definition = review_list[index]
        
        print(f"{word}\n")
        print(definition)
        print("\nUse → (Right) or ↓ (Down) for next, ← (Left) or ↑ (Up) for previous.")

        while True:
            key = keyboard.read_event().name  # Read keyboard input
            
            if key in ["right", "down"]:
                if index < len(review_list) - 1:
                    index += 1  # Move forward
                break  # Exit loop and update screen
            
            elif key in ["left", "up"]:
                if index > 0:
                    index -= 1  # Move backward
                break  # Exit loop and update screen

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
    vocab_dict = load_vocabularies(script_dir)
    
    if not vocab_dict:
        print("No valid vocabulary files found in the folder.")
        return
    
    review_vocabularies(vocab_dict)

if __name__ == '__main__':
    main()