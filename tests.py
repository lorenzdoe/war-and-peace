import unittest
from main import clean_word, transform_chapter, calc_raw_density, calc_av_space

class TestTransformFunctions(unittest.TestCase):

    def test_transform(self):
        self.assertEqual(clean_word('word'), 'word')
        self.assertEqual(clean_word('Word.'), 'word')
        self.assertEqual(clean_word('Wo-rd!?'), 'word')

    def test_transform_chapter(self):
        # Arrange
        chapter = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
        transformed_chapter = [(1, 'A'), (3, 'A'), (5, 'B'), (7, 'B')]
        key_dict = {
            'one': 'A',
            'three': 'A',
            'five': 'B',
            'seven': 'B'
        }

        # Act
        transformed = transform_chapter(key_dict)(chapter)

        # Assert
        self.assertEqual(transformed, transformed_chapter)

class TestCalculateFunctions(unittest.TestCase):
    def test_calc_raw_density(self):
        # Arrange
        transformed = [(1, 1), (2, 1), (3, 1), (4, 0), (5, 0), (7, 0), (8, 1)]
        filtered_ones = [(1, 1), (2, 1), (3, 1), (8, 1)]
        filtered_zeros = [(4, 0), (5, 0), (7, 0)]

        # Act
        ones_density = calc_raw_density(filtered_ones, transformed)
        zeros_density = calc_raw_density(filtered_zeros, transformed)

        # Assert
        self.assertEqual(ones_density, 4/7)
        self.assertEqual(zeros_density, 3/7)

    def test_calc_av_space(self):
        # Arrange
        ones = [(1, 1), (2, 1), (3, 1), (8, 1)]
        zeros = [(4, 0), (5, 0), (7, 0)]

        # Act
        ones_av_space = calc_av_space(ones)
        zeros_av_space = calc_av_space(zeros)

        # Assert
        self.assertEqual(ones_av_space, (1+1+5)/3)
        self.assertEqual(zeros_av_space, (1+2)/2)

if __name__ == '__main__':
    unittest.main()