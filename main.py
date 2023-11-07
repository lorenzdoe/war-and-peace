import subprocess
import concurrent.futures
import time
from itertools import islice, groupby
from enum import Enum
from typing import List, Tuple, Iterable, Generator, Iterator, Dict

### lambda functions ###

read_keywords = lambda filename: open(filename, 'r').read().splitlines()

# returns list of words
read_and_split = lambda filename: open(filename, 'r').read().split()

create_wordlist = lambda war_words, peace_words: (
    {word: WarOrPeace.WAR for word in war_words} | {word: WarOrPeace.PEACE for word in peace_words}
)

get_wordlist = lambda: create_wordlist(read_keywords('in/war.in'), read_keywords('in/peace.in'))

# transform word to lowercase and remove non-alphabetic characters
clean_word = lambda word: ''.join(c for c in word if c.isalpha()).lower()

### classes ###

class WarOrPeace(Enum):
    WAR = 0
    PEACE = 1

### functions ###

def get_chapters(book: List[str], keyword: str) -> List[List[str]]:
    is_chapter = lambda x: x == keyword
    # group words by chapters
    chapters: Generator[Iterator] = (grouper for key, grouper in groupby(book, key=is_chapter) if not key)
    # TODO :: remove very last part of the last chapter
    # 
    # transform words to lowercase and remove non-alphabetic characters
    only_words_chapters: Generator = (list(map(clean_word, chapter)) for chapter in chapters)
    return list(islice(only_words_chapters, 1, None)) # skip text before chapter 1 using islice

# transforms a chapter to a list of tuples (word_index, PEACE or WAR), not classified words are ignored
def transform_chapter(key_dict) -> List[Tuple]:
    return lambda chapter: [(i, key_dict[word]) for i, word in enumerate(chapter) if word in key_dict]

# gets a chapter and returns a dictionary with key is either war or peace and value is a tuple of indices
def map_chapter(key_dict: Dict[str, Enum], chapter: List[str]) -> Dict[Enum, Tuple[int]]:
    transformed_chapter = transform_chapter(key_dict)(chapter)
    return {
        WarOrPeace.WAR: tuple(i for i, WoP in transformed_chapter if WoP is WarOrPeace.WAR),
        WarOrPeace.PEACE: tuple(i for i, WoP in transformed_chapter if WoP is WarOrPeace.PEACE)
    }

if __name__ == '__main__':
    #subprocess.run(['python3', 'tests.py'], check=True)

    wordlist: dict = get_wordlist()
    war_and_peace: List[str] = read_and_split('in/war_and_peace.in')
    chapters: List[List[str]] = get_chapters(book=war_and_peace,keyword='CHAPTER')
    transformed_chapters = [transform_chapter(wordlist)(chapter) for chapter in chapters]

    chapter0 = transformed_chapters[0]
    
    mapped_chapter0 = map_chapter(wordlist, chapters[0])

    print(mapped_chapter0)

    # for i, chapter in enumerate(transformed_chapters):
    #     print(f"Chapter {i+1}: {tuple(chapter)}")

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for i, (chap, score) in enumerate(zip(transformed_chapters, executor.map(calc_chapter_relation, transformed_chapters))):
    #         print(f"Chapter {i+1}: {score.name}")
