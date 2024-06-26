from unittest import TestCase
from gluepy.utils.loading import empty


class ContextTestCase(TestCase):

    def test_context_populated(self):
        from gluepy.conf import default_context
        # default_context is not evaluated yet.
        self.assertEqual(default_context._wrapped, empty)
        # When we try to access a param, it is being populated by our ``context.yaml``
        self.assertEqual(default_context.foo, 1)
        # It is now fully evaluated and no longer lazy.
        self.assertNotEqual(default_context._wrapped, empty)
