from unittest import TestCase
from gluepy.utils.loading import SingletonMixin


class LoadingTestCase(TestCase):
    def test_singleton(self):
        class NotSingleton:
            """Can exist multiple instance of this class"""

        class MySingleton(SingletonMixin):
            """Can only exist 1 instance of this class"""

        s1, ns1 = MySingleton(), NotSingleton()
        s2, ns2 = MySingleton(), NotSingleton()

        self.assertTrue(s1 is s2)
        self.assertFalse(ns1 is ns2)
