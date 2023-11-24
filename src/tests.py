import pytest
from main import clean_word, transform_chapter, map_chapter, calc_av_space

def test_clean_word():
    assert clean_word('word') == 'word'
    assert clean_word('Word.') == 'word'
    assert clean_word('Wo-rd!?') == 'word'

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
    mapped = map_chapter(sample_key_dict, sample_chapter, 1, 'A', 'B')
    # Assert
    assert mapped == {
        'nr': 1,
        'len': 9,
        'A': (1, 3, 8),
        'B': (5, 7)
    }

def test_calc_av_space(sample_chapter, sample_key_dict):
    # Arrange
    mapped = map_chapter(sample_key_dict, sample_chapter, 1, 'A', 'B')
    mapped_2 = map_chapter({'zero': 'A'}, ['zero'], 1, 'A', 'B')
    mapped_3 = map_chapter({'zero':'A', 'one':'A', 'two':'A', 'three': 'A'}, ['zero', 'one', 'two', 'three'], 1, 'A', 'B')
    # Act
    av_space_A = calc_av_space(mapped['A'])
    av_space_B = calc_av_space(mapped['B'])
    av_space_2_A = calc_av_space(mapped_2['A'])
    av_space_2_B = calc_av_space(mapped_2['B'])
    av_space_3_A = calc_av_space(mapped_3['A'])
    # Assert
    assert av_space_A == ((3-1) + (8-3)) / 2
    assert av_space_B == (7-5)
    assert av_space_2_A == None
    assert av_space_2_B == None
    assert av_space_3_A == 1
