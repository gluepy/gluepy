from unittest import TestCase
from box.exceptions import BoxError
from gluepy.utils.loading import empty
from gluepy.conf.context import Context


class ContextTestCase(TestCase):
    def setUp(self):
        from gluepy.conf import default_context, default_context_manager

        # Reset the lazy proxy so default_context starts unevaluated
        default_context._wrapped = empty
        # Reset the context manager's cached context
        default_context_manager._wrapped = empty
        # Reset the singleton so a fresh Context is created
        Context._Context__singleton_instance = None
        return super().setUp()

    def test_context_populated(self):
        from gluepy.conf import default_context

        # default_context is not evaluated yet.
        self.assertEqual(default_context._wrapped, empty)
        # When we try to access a param, it is being populated by our ``context.yaml``
        self.assertEqual(default_context.foo, 1)
        # It is now fully evaluated and no longer lazy.
        self.assertNotEqual(default_context._wrapped, empty)

    def test_context_read_only_top_level(self):
        from gluepy.conf import default_context

        # Force evaluation
        _ = default_context.foo
        with self.assertRaises(TypeError):
            default_context.foo = "bar"

    def test_context_read_only_nested(self):
        from gluepy.conf import default_context

        # Force evaluation
        _ = default_context.gluepy.run_id
        with self.assertRaises(BoxError):
            default_context.gluepy.run_id = "new"

    def test_context_read_only_nested_setitem(self):
        from gluepy.conf import default_context

        # Force evaluation
        _ = default_context.gluepy.run_id
        with self.assertRaises(BoxError):
            default_context.gluepy["run_id"] = "new"

    def test_context_local_patches_merged(self):
        from gluepy.conf.context import DefaultContextManager

        mgr = DefaultContextManager()
        ctx = mgr.create_context(local_patches=[{"custom_key": "custom_value"}])
        self.assertEqual(ctx.custom_key, "custom_value")

    def test_context_local_patches_precedence(self):
        from gluepy.conf.context import DefaultContextManager

        mgr = DefaultContextManager()
        # Local patches should override base config values.
        # Base context.yaml has foo: 1, local patch sets foo: 999.
        ctx = mgr.create_context(local_patches=[{"foo": 999}])
        self.assertEqual(ctx.foo, 999)
