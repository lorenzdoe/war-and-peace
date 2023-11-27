import pytest
from hypothesis import given
from hypothesis import strategies as st

from main import clean_word, transform_chapter, map_chapter, calc_av_space, calc_score, split_into_chapters

## Hypothesis is a library for property based testing. It generates random input for the test function.

def test_clean_word():
    assert clean_word('word') == 'word'
    assert clean_word('Word.') == 'word'
    assert clean_word('Wo-rd!?') == 'word'
    assert clean_word('".-!?') == ''

@pytest.fixture
def sample_chapter():
    return ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']

@pytest.fixture
def sample_key_dict():
    return {
        'one': 'A',
        'three': 'A',
        'eight': 'A',
        'five': 'B',
        'seven': 'B'
    }

def test_transform_chapter(sample_chapter, sample_key_dict):
    # Act
    transformed = transform_chapter(sample_key_dict)(sample_chapter)
    # Assert
    assert transformed == ((1, 'A'), (3, 'A'), (5, 'B'), (7, 'B'), (8, 'A'))

def test_map_chapter(sample_chapter, sample_key_dict):
    # Act
    mapped_sample = map_chapter(sample_key_dict, sample_chapter, 1, 'A', 'B')
    mapped_2 = map_chapter({'zero': 'A'}, ['zero'], 1, 'A', 'B')
    mapped_3 = map_chapter({'zero':'A', 'one':'A', 'two':'A', 'three': 'A'}, ['zero', 'one', 'two', 'three'], 1, 'A', 'B')
    # Assert
    assert mapped_sample == {
        'nr': 1,
        'len': 9,
        'A': (1, 3, 8),
        'B': (5, 7) }
    assert mapped_2 == {'nr': 1, 'len': 1, 'A': (0,), 'B': ()}
    assert mapped_3 == {'nr': 1, 'len': 4, 'A': (0, 1, 2, 3), 'B': ()}

def test_calc_av_space(sample_chapter, sample_key_dict):
    # Arrange
    mapped = {'nr': 1, 'len': 9, 'A': (1, 3, 8), 'B': (5, 7)}
    mapped_2 = {'nr': 1, 'len': 1, 'A': (0,), 'B': ()}
    mapped_3 = {'nr': 1, 'len': 4, 'A': (0, 1, 2, 3), 'B': ()}
    test_tuple = (1,2,3,4,5)
    # Act
    av_space_A = calc_av_space(mapped['A'])
    av_space_B = calc_av_space(mapped['B'])
    av_space_2_A = calc_av_space(mapped_2['A'])
    av_space_2_B = calc_av_space(mapped_2['B'])
    av_space_3_A = calc_av_space(mapped_3['A'])
    av_space_d = calc_av_space(test_tuple)
    # Assert
    assert av_space_A == ((3-1) + (8-3)) / 2
    assert av_space_B == (7-5)
    assert av_space_2_A == None
    assert av_space_2_B == None
    assert av_space_3_A == 1
    assert av_space_d == 1

# Property based testing with hypothesis
# @given is part of hypothesis, it generates random input for the test function

@given(st.lists(st.text()), st.text(min_size=1))
def test_split_into_chapters(sample_book, keyword):
    # Act
    chapters = split_into_chapters(sample_book, keyword)
    # Assert
    assert all(keyword not in chapter for chapter in chapters)

@given(st.tuples(st.integers()))
def test_calc_av_space_property_based(indices):
    # Act
    av_space = calc_av_space(indices)
    # Assert
    if len(indices) > 1:
        assert av_space >= 1
    else:
        assert av_space == None

@given(st.tuples(st.integers()), st.integers(min_value=0))
def test_calc_score_property(indices, chap_len):
    # Act
    score = calc_score(indices, chap_len)
    # Assert
    assert score >= 0
    