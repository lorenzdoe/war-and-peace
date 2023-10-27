import subprocess
from itertools import accumulate, takewhile, dropwhile, islice, groupby
from enum import Enum
from typing import List, Dict, Tuple, Set, Iterable, Callable, Any, Union, Generator

read_war = lambda: open('in/war.in', 'r').read().splitlines()

read_peace = lambda: open('in/peace.in', 'r').read().splitlines()

create_wordlist = lambda war_words, peace_words: (
    {word: WarOrPeace.WAR for word in war_words} | {word: WarOrPeace.PEACE for word in peace_words}
)

get_wordlist = lambda: create_wordlist(read_war(), read_peace())

# returns list of words
read_war_and_peace = lambda: open('in/war_and_peace.in', 'r').read().split()

# transform word to lowercase and remove non-alphabetic characters
transform_word = lambda word: ''.join(c for c in word if c.isalpha()).lower()

class WarOrPeace(Enum):
    WAR = 0
    PEACE = 1

def get_chapters(war_and_peace: List[str]) -> List[List[str]]:
    is_chapter = lambda x: x == 'CHAPTER'
    # group words by chapters
    chapters: Iterable[Generator] = (g for k, g in groupby(war_and_peace, key=is_chapter) if not k)
    # TODO :: remove very last part of the last chapter
    # transform words to lowercase and remove non-alphabetic characters
    only_words_chapters: Generator = (list(map(transform_word, chapter)) for chapter in chapters)
    return list(islice(only_words_chapters, 1, None)) # skip first chapter using islice


if __name__ == '__main__':
    subprocess.run(['python3', 'tests.py'], check=True)

    wordlist: dict = get_wordlist()
    war_and_peace: List[str] = read_war_and_peace()
    chapters: List[List[str]] = get_chapters(war_and_peace)

    print('War and Peace has {} chapters'.format(len(chapters)))
    print(chapters[0])
    print(chapters[len(chapters) - 1])
