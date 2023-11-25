from itertools import groupby
from enum import Enum
from typing import List, Tuple, Generator, Iterator, Dict
from functools import partial

from Monad import Maybe

space_weight = 1
density_weight = 1

def read_and_apply(filename: str, func) -> Maybe:
    """
    Reads a file and applies a function to it
    returns List[str]
    """
    try:
        content = open(filename, 'r').read()
        return Maybe(func(content))
    except Exception as e:
        return Maybe(None, is_error=True)

# read a file and split it into lines, returns List[str]
read_keywords = partial(read_and_apply, func=lambda x: x.splitlines())

# read a file and split it into words, returns List[str]
read_and_split = partial(read_and_apply, func=lambda x: x.split())

create_wordlist = lambda war_words, peace_words: (
    {word: WarOrPeace.WAR for word in war_words} | {word: WarOrPeace.PEACE for word in peace_words}
)

def read_wordlists(war_file: str, peace_file: str)-> Maybe:
    """
    produces a dictionary with key is a word and value is either WAR or PEACE
    """
    war_keywords = read_keywords(war_file)
    peace_keywords = read_keywords(peace_file)
    
    if war_keywords.is_error or peace_keywords.is_error:
        return Maybe(None, is_error=True)
    
    return Maybe(create_wordlist(war_keywords.value, peace_keywords.value))

# transform word to lowercase and remove non-alphabetic characters
clean_word = lambda word: ''.join(c for c in word if c.isalpha()).lower()

class WarOrPeace(Enum):
    WAR = 0
    PEACE = 1


def split_into_chapters(book: List[str], keyword: str) -> Tuple[Tuple[str]]:
    """
    Takes List[str] and splits it into chapters by keyword
    """
    is_chapter = lambda x: x == keyword
    # group words by chapters
    chapters: Generator[Iterator] = (grouper for key, grouper in groupby(book, key=is_chapter) if not key)
    # transform words to lowercase and remove non-alphabetic characters
    only_words_chapters: Generator = (tuple(map(clean_word, chapter)) for chapter in chapters)
    # skip text before chapter 1
    return tuple(only_words_chapters)[1:]


def transform_chapter(key_dict) -> Tuple[Tuple]:
    """
    transforms a chapter to a tuple of tuples (word_index, PEACE or WAR), not classified words are ignored
    """
    return lambda chapter: tuple((i, key_dict[word]) for i, word in enumerate(chapter) if word in key_dict)


def filter_transformed_chapter(transformed_chapter: Tuple[Tuple], key) -> Tuple[Tuple]:
    """
    filter out words that are classified as key
    """
    return tuple(i for i, c_key in transformed_chapter if c_key is key)


def calc_av_space(indices: Tuple[int]) -> float:
    """
    calculates the average space between words in a chapter
    """
    return None if len(indices) <= 1 else sum(indices[i+1] - indices[i] for i in range(len(indices)-1)) / (len(indices)-1)


def map_chapter(key_dict: Dict[str, Enum], chapter: List[str], chapter_nr: int, type1, type2) -> Dict[Enum, Tuple[int]]:
    """
    map step from map reduce.
    returns a dict, where key is chapter nr. and value is a tuple of indices of words, all classified as the same type
    """
    transformed_chapter = transform_chapter(key_dict)(chapter)
    return {
        'nr': chapter_nr,
        'len': len(chapter),
        type1: filter_transformed_chapter(transformed_chapter, type1),
        type2: filter_transformed_chapter(transformed_chapter, type2)
    }

# bind map_chapter to specific types
map_chapter_WoP = partial(map_chapter, type1=WarOrPeace.WAR, type2=WarOrPeace.PEACE)

def calc_score(indices: Tuple[int], chap_len: int) -> float:
    """
    returns a tuple with chapter nr. and score for that chapter
    """
    av_space: float = calc_av_space(indices)
    space_score: float = (1 / av_space) if av_space is not None else 0
    density_score: float = len(indices) / chap_len
    return (space_weight * space_score + density_weight * density_score ) * 100

def shuffle_chapters(chapters: Tuple[Dict[Enum, Tuple[int]]], type) -> Tuple[float]:
    """
    shuffle step from map reduce, returns a list of tuples with scores for that chapter
    """
    return tuple(calc_score(chapter[type], chapter['len']) for chapter in chapters)


def print_results(reduced_chapters: List[Enum]) -> None:
    for i, chapter in enumerate(reduced_chapters):
        print(f'Chapter {i+1}: {chapter.name.lower()}-related')


if __name__ == '__main__':

    maybe_wordlist: Maybe = read_wordlists('in/war.in', 'in/peace.in')
    maybe_war_and_peace: Maybe = read_and_split('in/war_and_peace.in')

    if maybe_wordlist.is_error or maybe_war_and_peace.is_error:
        print('Error reading files')
        exit(1)

    wordlist: dict = maybe_wordlist.value
    war_and_peace: Tuple[str] = maybe_war_and_peace.value

    chapters: Tuple[List[str]] = split_into_chapters(book=war_and_peace,keyword='CHAPTER')
    transformed_chapters = tuple(transform_chapter(wordlist)(chapter) for chapter in chapters)

    # map
    mapped_chapters: Dict = tuple(map_chapter_WoP(wordlist, chapter, i+1) for i, chapter in enumerate(chapters))

    # "shuffle"
    war_scores: Tuple[float] = shuffle_chapters(mapped_chapters, WarOrPeace.WAR)
    peace_scores: Tuple[float] = shuffle_chapters(mapped_chapters, WarOrPeace.PEACE)

    # reduce
    reduced: Tuple[Enum] = tuple(WarOrPeace.WAR if war_score > peace_score else WarOrPeace.PEACE for war_score, peace_score in zip(war_scores, peace_scores))
    
    print_results(reduced)
