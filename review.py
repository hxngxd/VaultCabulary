#!/usr/bin/env python3
import os
import random
import re
import keyboard  # pip install keyboard

def clean_markdown(text):
    """
    Remove markdown formatting tokens from the text:
      - Removes header markers (e.g., ###)
      - Removes emphasis markers (e.g., ***, **, *, __, _)
    """
    # Remove markdown header markers at the beginning of lines
    text = re.sub(r'^(#{1,6}\s*)', '', text, flags=re.MULTILINE)
    # Remove emphasis markers: any sequence of *, or _
    text = re.sub(r'(\*\*\*|\*\*|\*|__|_)', '', text)
    return text

def parse_markdown_file(filepath):
    """
    Parses a markdown file and extracts the vocabulary word and its definition blocks.
    Expected format: a header line with "# word" and definition blocks separated by '---'.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the word (first line starting with "# ")
    word_match = re.search(r'^#\s*(.+)', content, re.MULTILINE)
    if not word_match:
        return None
    word = word_match.group(1).strip()
    
    # Split content into blocks using '---' as the delimiter
    blocks = re.split(r'\n---\n', content)
    
    # Extract blocks that look like definitions (containing keywords like "Examples:", "Synonyms:", or "Antonyms:")
    defs = [block.strip() for block in blocks if re.search(r'(Examples:|Synonyms:|Antonyms:)', block)]
    
    return word, defs if defs else None

def load_vocabularies(folder):
    """
    Loads all .md files in the specified folder, parsing each for vocabulary words and their definitions.
    Returns a dictionary {word: [definitions]}.
    """
    vocab_dict = {}
    for filename in os.listdir(folder):
        if filename.endswith('.md'):
            filepath = os.path.join(folder, filename)
            parsed = parse_markdown_file(filepath)
            if parsed:
                word, defs = parsed
                if defs:
                    vocab_dict[word] = defs[:]  # copy list of definitions
    return vocab_dict

def build_slides(vocab_dict):
    """
    Builds a list of slides. Each slide is a tuple (word, definition).
    Each definition for every word will appear exactly once.
    The list is then randomized.
    """
    slides = []
    for word, defs in vocab_dict.items():
        for d in defs:
            slides.append((word, d))
    random.shuffle(slides)
    return slides

def wait_for_key_release():
    """
    Waits until a key-release (KEY_UP) event is detected,
    ignoring all KEY_DOWN events.
    Returns the released event.
    """
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP:
            return event

def review_slides(slides):
    """
    Allows navigation through the slides:
      - Press Enter (release) for next slide.
      - Press Shift+Enter (release) for previous slide.
      - Press Esc (release) to exit.
    The slide is updated only on key release.
    """
    current_index = 0
    total = len(slides)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        word, definition = slides[current_index]
        # Clean the markdown formatting before displaying
        clean_word = clean_markdown(word)
        clean_def = clean_markdown(definition)
        
        print(f"{clean_word}\n")
        print(clean_def)
        print(f"\nSlide {current_index+1} of {total}")
        print("Press Enter for next, Shift+Enter for previous, Esc to exit.")
        
        # Wait for a key-release event (ignoring KEY_DOWN events)
        event = wait_for_key_release()
        
        if event.name == 'esc':
            break
        elif event.name == 'enter':
            # Determine if Shift is pressed at the moment of key release.
            if keyboard.is_pressed('shift'):
                if current_index > 0:
                    current_index -= 1
            else:
                if current_index < total - 1:
                    current_index += 1
                else:
                    print("\nYou've reached the end of the slides. Exiting...")
                    break

def main():
    # Use the script's directory (assumes Markdown files are in the same folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vocab_dict = load_vocabularies(script_dir)
    
    if not vocab_dict:
        print("No valid vocabulary files found in the folder.")
        return
    
    slides = build_slides(vocab_dict)
    review_slides(slides)
    print("Review complete!")

if __name__ == '__main__':
    main()
