from unittest import TestCase, main
from src.string_comparer.simhash_comparer import SimhashComparer

class TestSimhash(TestCase):
    def test_return_100_when_identical(self):
        str1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla sed tortor in est facilisis viverra ut quis nisl.
        Morbi at scelerisque quam. Vivamus vitae neque faucibus, cursus ligula vel, eleifend sem.
        In hac habitasse platea dictumst. Etiam gravida massa sit amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget elementum est. Sed rutrum sagittis nisl, ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet. Donec auctor tortor et augue consectetur mollis.
        Integer in volutpat erat."""
        str2 = str(str1)
        self.assertEqual(SimhashComparer.compare(str1, str2), 100.0)

    def test_when_similar_but_more_new_lines_and_whitespaces(self):
        str1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla sed tortor in est facilisis viverra ut quis nisl.
        Morbi at scelerisque quam. Vivamus vitae neque faucibus, cursus ligula vel, eleifend sem.
        In hac habitasse platea dictumst. Etiam gravida massa sit amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget elementum est. Sed rutrum sagittis nisl, ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet. Donec auctor tortor et augue consectetur mollis.
        Integer in volutpat erat."""
        str2 = """Lorem ipsum dolor sit amet,
        consectetur adipiscing elit.
        Nulla sed tortor in est                            facilisis viverra ut quis nisl.
        Morbi at scelerisque quam. Vivamus vitae neque faucibus,
         cursus ligula vel, eleifend sem.
            In hac habitasse platea dictumst.
        Etiam gravida massa sit         amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget         elementum est.
        Sed rutrum sagittis nisl,                ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet.
        Donec auctor tortor et         augue consectetur mollis.Integer in volutpat erat."""
        self.assertEqual(SimhashComparer.compare(str1, str2), 100.0)

    def test_when_similar_but_few_words_changed(self):
        str1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla sed tortor in est facilisis viverra ut quis nisl.
        Morbi at scelerisque quam. Vivamus vitae neque faucibus, cursus ligula vel, eleifend sem.
        In hac habitasse platea dictumst. Etiam gravida massa sit amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget elementum est. Sed rutrum sagittis nisl, ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet. Donec auctor tortor et augue consectetur mollis.
        Integer in volutpat erat."""
        str2 = """Gigo ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla sed tortor in est facilisis viverra ut quis nisl.
        Morbi at vigo quam. Vivamus vitae neque faucibus, cursus ligula vel, eleifend sem.
        In hac habitasse platea dictumst. Etiam tigo massa sit amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget rigo est. Sed rutrum sagittis nisl, ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet. Vertigo auctor tortor et augue consectetur mollis.
        Integer in volutpat ерат."""
        self.assertAlmostEqual(SimhashComparer.compare(str1, str2), 76.7, 1)

    def test_when_completely_different(self):
        str1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla sed tortor in est facilisis viverra ut quis nisl.
        Morbi at scelerisque quam. Vivamus vitae neque faucibus, cursus ligula vel, eleifend sem.
        In hac habitasse platea dictumst. Etiam gravida massa sit amet ante vehicula, vel volutpat augue varius.
        Nulla vel mollis ante, eget elementum est. Sed rutrum sagittis nisl, ac bibendum ligula dictum sit amet.
        Cras gravida varius turpis sit amet imperdiet. Donec auctor tortor et augue consectetur mollis.
        Integer in volutpat erat.
        """
        str2 = """Vestibulum aliquam velit aliquam eros semper fringilla. Maecenas feugiat efficitur arcu nec sodales. Etiam feugiat, justo vitae cursus elementum, erat massa elementum nibh, vitae congue tortor eros a libero. Pellentesque id urna sem. Cras ipsum ligula, cursus quis vulputate in, iaculis vitae ante. Quisque tempor ut felis vel semper. Donec lacinia, metus vitae scelerisque dictum, nulla tortor porta odio, id fermentum massa tortor eget mi. Curabitur ullamcorper eget enim eget consequat. Nullam viverra turpis at sagittis efficitur. Aenean nec arcu commodo, consequat eros eu, gravida massa. Etiam finibus diam magna, id auctor magna feugiat ut. Pellentesque faucibus scelerisque lectus, eget pretium felis semper sit amet. Aenean eros est, congue non pharetra vulputate, lacinia non lectus."""
        self.assertEqual(SimhashComparer.compare(str1, str2), 30.0)

if __name__ == '__main__':
    main()
