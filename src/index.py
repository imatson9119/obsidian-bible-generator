import os
from src.constants import book_abbreviations, abbv_to_full
import json


'''
The purpose of this script is to generate a Bible in markdown for use in obsidian.
'''

use_cross_refs = False
file_for_verse = False

def main():
  with open('data/esv-bible.json', 'r') as file:
    data = json.loads(file.read())
  with open('data/cross-references.json', 'r') as file:
    cross_refs = json.loads(file.read())
  
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
      book_file.write(create_book(book_name, data, i))
    for j, chapter in enumerate(data[book_name]):
      if file_for_verse:
        chapter_folder_name = f'{book_folder}/{j+1}'
        os.mkdir(chapter_folder_name)
        for k, verse in data[book_name][chapter].items():
          verse_file_name = f'{chapter_folder_name}/{book_name} {chapter} {k}.md'
          with open(verse_file_name, 'w') as verse_file:
            verse_file.write(create_verse(book_name, chapter, k, data, cross_refs, i))
      else:
        chapter_file_name = f'{book_folder}/{book_name} {j+1}.md'
        with open(chapter_file_name, 'w') as chapter_file:
          chapter_file.write(create_chapter(book_name, chapter, data, cross_refs, i))
  


def get_short_book_link(book_name):
  return f'[[{book_name}|{book_abbreviations[book_name.lower()]}]]' 

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
{'\n'.join([f'[[--{n}--|{n}]]' for n in list(bible_data.keys())[:39]])}

## New Testament
{'\n'.join([f'[[--{n}--|{n}]]' for n in list(bible_data.keys())[39:]])}
'''
  return bible

def create_book(book_name, bible_data, i):
  book = f'''---
aliases:
  - {book_abbreviations[book_name.lower()]}
  - {book_name}
tags:
  - bible/book
  - bible/{book_name}
  - bible/{'old testament' if i < 39 else 'new testament'}
cssclass:
  - bible
---

# {book_name}

## Chapters

{'\n'.join([f'[[{book_name} {i+1}|{i+1}]]' for i in range(len(bible_data[book_name]))])}
'''
  return book

def get_cross_references(book_name, chapter_number, verse_number, cross_refs):
  
  if use_cross_refs and book_name in cross_refs and chapter_number in cross_refs[book_name] and verse_number in cross_refs[book_name][chapter_number]:
    if file_for_verse:
      return f'{", ".join([f'[[{book} {chapter} {verse}]]' for book, chapter, verse in cross_refs[book_name][chapter_number][verse_number]])}\n'
    return f'{", ".join([f"[[{book} {chapter}#{verse}]]" for book, chapter, verse in cross_refs[book_name][chapter_number][verse_number]])}\n'
  return ''
  
def create_chapter(book_name, chapter_number, bible_data, cross_refs, i):
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
  - bible/{'old testament' if i < 39 else 'new testament'}
cssclass:
  - bible
---

# {book_name} {chapter_number}

{''.join(
  [
    f'###### {i}\n{x.strip()}\n' + 
      get_cross_references(book_name, chapter_number, i, cross_refs)
    for i,x in bible_data[book_name][chapter_number].items()
  ])}

'''

  return chapter

def create_verse(book_name, chapter_number, verse_number, bible_data, cross_refs, i):
  verse = f'''---
aliases:
  - {book_abbreviations[book_name.lower()]} {chapter_number} {verse_number}
  - {book_name} {chapter_number} {verse_number}
  - {book_abbreviations[book_name.lower()]}.{chapter_number}.{verse_number}
  - {book_name}.{chapter_number}.{verse_number}
  - {book_abbreviations[book_name.lower()]}-{chapter_number}-{verse_number}
  - {book_name}-{chapter_number}-{verse_number}
  - {book_abbreviations[book_name.lower()]}_{chapter_number}_{verse_number}
  - {book_name}_{chapter_number}_{verse_number}
  - {book_abbreviations[book_name.lower()]} {chapter_number}.{verse_number}
  - {book_name} {chapter_number}.{verse_number}
  - {book_abbreviations[book_name.lower()]} {chapter_number}-{verse_number}
  - {book_name} {chapter_number}-{verse_number}
  - {book_abbreviations[book_name.lower()]} {chapter_number}_{verse_number}
  - {book_name} {chapter_number}_{verse_number}
tags:
  - bible/verse
  - bible/{book_name}/verse
  - bible/{book_name}/{chapter_number}/verse
  - bible/{book_name}/{chapter_number}/{verse_number}
  - bible/{'old testament' if i < 39 else 'new testament'}
cssclass:
  - bible
---

# {book_name} {chapter_number}:{verse_number}

{bible_data[book_name][chapter_number][verse_number]}

{get_cross_references(book_name, chapter_number, verse_number, cross_refs)}
'''
  return verse


if __name__ == "__main__":
  main()