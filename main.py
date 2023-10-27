import subprocess
import concurrent.futures
import time
from itertools import islice, groupby
from enum import Enum
from typing import List, Tuple, Iterable, Generator

### lambda functions ###

read_war = lambda: open('in/war.in', 'r').read().splitlines()

read_peace = lambda: open('in/peace.in', 'r').read().splitlines()

create_wordlist = lambda war_words, peace_words: (
    {word: WarOrPeace.WAR for word in war_words} | {word: WarOrPeace.PEACE for word in peace_words}
)

get_wordlist = lambda: create_wordlist(read_war(), read_peace())

# returns list of words
read_war_and_peace = lambda: open('in/war_and_peace.in', 'r').read().split()

# transform word to lowercase and remove non-alphabetic characters
clean_word = lambda word: ''.join(c for c in word if c.isalpha()).lower()

# filter transformed chapter by WarOrPeace
filter_tchapter = lambda tchapter: lambda WoP: list(filter(lambda x: x[1] is WoP, tchapter))

# calculate the overall density of filtered words in chapter
calc_raw_density = lambda filtered_tchap, tchap: len(filtered_tchap) / len(tchap)

### classes ###

class WarOrPeace(Enum):
    WAR = 0
    PEACE = 1

### functions ###

def get_chapters(war_and_peace: List[str]) -> List[List[str]]:
    is_chapter = lambda x: x == 'CHAPTER'
    # group words by chapters
    chapters: Iterable[Generator] = (g for k, g in groupby(war_and_peace, key=is_chapter) if not k)
    # TODO :: remove very last part of the last chapter
    # transform words to lowercase and remove non-alphabetic characters
    only_words_chapters: Generator = (list(map(clean_word, chapter)) for chapter in chapters)
    return list(islice(only_words_chapters, 1, None)) # skip first chapter using islice

# transforms a chapter to a list of tuples (word_index, PEACE or WAR)
def transform_chapter(key_dict) -> List[Tuple]:
    return lambda chapter: [(i, key_dict[word]) for i, word in enumerate(chapter) if word in key_dict]

# takes a filtered transformed chapter and returns the average space between words
def calc_av_space(filtered_tchap: List[Tuple]) -> float:
    denominator = 1 if len(filtered_tchap) == 1 else len(filtered_tchap)-1
    return sum(y[0] - x[0] for x, y in zip(filtered_tchap[:-1], filtered_tchap[1:])) / denominator

# calulates the score (average space * raw_density) from transformed chapter
def calc_score(tchap, WoP):
    filtered_tchap = filter_tchapter(tchap)(WoP)
    return calc_av_space(tchap) * calc_raw_density(filtered_tchap, tchap)

def calc_chapter_relation(tchap):
    war_score = calc_score(tchap, WarOrPeace.WAR)
    peace_score = calc_score(tchap, WarOrPeace.PEACE)
    return WarOrPeace.WAR if war_score > peace_score else WarOrPeace.PEACE

if __name__ == '__main__':
    subprocess.run(['python3', 'tests.py'], check=True)

    wordlist: dict = get_wordlist()
    war_and_peace: List[str] = read_war_and_peace()
    chapters: List[List[str]] = get_chapters(war_and_peace)
    transformed_chapters = [transform_chapter(wordlist)(chapter) for chapter in chapters]

    # start_time = time.time()

    # for i, tchap in enumerate(transformed_chapters):
    #     print(f"Chapter {i+1}: {calc_chapter_relation(tchap).name}")

    # time1 = time.time() - start_time

    # start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, (chap, score) in enumerate(zip(transformed_chapters, executor.map(calc_chapter_relation, transformed_chapters))):
            print(f"Chapter {i+1}: {score.name}")

    # time2 = time.time() - start_time

    # print(f"Non-concurrent method took {time1} seconds.")
    # print(f"Concurrent method took {time2} seconds.")

