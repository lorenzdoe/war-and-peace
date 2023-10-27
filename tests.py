import unittest
from main import transform_word

class TestTransformWord(unittest.TestCase):
    def test_transform(self):
        self.assertEqual(transform_word('word'), 'word')
        self.assertEqual(transform_word('Word.'), 'word')
        self.assertEqual(transform_word('Wo-rd!?'), 'word')

if __name__ == '__main__':
    unittest.main()