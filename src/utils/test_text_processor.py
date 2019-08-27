from unittest import TestCase, main
from .text_processor import get_topn_words, get_cosine_sim

class TestGetTopNWords(TestCase):
    def test_should_return_top3_w(self):
        text = 'AI and humans have always been friendly with AI AI AI and and have'
        actual = get_topn_words(text, 3)
        self.assertListEqual(actual, ['ai', 'and', 'have'])

class TestGetCosineSim(TestCase):
    def test_should_return_cosine_sim(self):
        texts = [
            'AI is our friend and it has been friendly',
            'AI and humans have always been friendly with AI AI AI and and have',
            'AI is not a human'
        ]
        actual = get_cosine_sim(texts)[0]
        self.assertAlmostEqual(actual[0], 1, 2,  '100 percent equality')
        self.assertAlmostEqual(actual[1], 0.5, 1, '50 percent equality')
        self.assertAlmostEqual(actual[2], 0.3, 1, '30 percent equality')

if __name__ == '__main__':
    main()
