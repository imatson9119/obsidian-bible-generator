import os
from src.constants import book_abbreviations
import json


'''
The purpose of this script is to generate a Bible in markdown for use in obsidian.
'''

def main():
  with open('data/esv-bible.json', 'r') as file:
    data = json.loads(file.read())
  print("Loaded Bible, beginning processing...")
  # remove output folder if it exists
  if os.path.exists('output'):
    os.system('rm -rf output')
  os.makedirs('output')

  with open('output/--bible--.md', 'w') as bible_file:
    bible_file.write(get_bible(data))
  for i, book_name in enumerate(data.keys()):
    book_folder = f'output/{i} {book_abbreviations[book_name.lower()]}'
    os.mkdir(book_folder)
    with open(f'{book_folder}/--{book_name}--.md', 'w') as book_file:
      book_file.write(create_book(book_name, data))
    for j, chapter in enumerate(data[book_name]):
      chapter_file_name = f'{book_folder}/{book_name} {j+1}.md'
      with open(chapter_file_name, 'w') as chapter_file:
        chapter_file.write(create_chapter(book_name, chapter, data))


    
  

def get_short_book_link(book_name):
  return f'[[{book_name}|{book_abbreviations[book_name]}]]' 

def get_bible(bible_data):
  bible = f'''---
aliases:
  - Bible
  - ESV
  - English Standard Version
  - Scripture
  - Scriptures
  - Word of God
  - Holy Bible
  - Holy Scriptures
  - Holy Word
  - Holy Writ
  - Holy Scripture
  - Gods Word
tags:
  - bible
cssclass:
  - bible
---

# Bible

## Old Testament
{'\n'.join([f'[[{n}]]' for n in list(bible_data.keys())[:39]])}

## New Testament
{'\n'.join([f'[[{n}]]' for n in list(bible_data.keys())[39:]])}
'''
  return bible

def create_book(book_name, bible_data):
  book = f'''---
aliases:
  - {book_abbreviations[book_name.lower()]}
tags:
  - bible/book
  - bible/{book_name}
cssclass:
  - bible
---

# {book_name}

## Chapters

{'\n'.join([f'[[{book_name} {i+1}|{i+1}]]' for i in range(len(bible_data[book_name]))])}
'''
  return book
  
def create_chapter(book_name, chapter_number, bible_data):
  chapter = f'''---
aliases:
  - {book_abbreviations[book_name.lower()]} {chapter_number}
  - {book_name}.{chapter_number}
  - {book_abbreviations[book_name.lower()]}.{chapter_number}
  - {book_name}-{chapter_number}
  - {book_abbreviations[book_name.lower()]}-{chapter_number}
  - {book_name}_{chapter_number}
  - {book_abbreviations[book_name.lower()]}_{chapter_number}
tags:
  - bible/chapter
  - bible/{book_name}/chapter
  - bible/{book_name}/{chapter_number}
cssclass:
  - bible
---

# {book_name} {chapter_number}

{''.join(
  [
    f'###### {x}\n{i.strip()}\n' for x,i in bible_data[book_name][chapter_number].items()
  ])}

'''

  return chapter

if __name__ == "__main__":
  main()