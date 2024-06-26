from unittest import TestCase
from gluepy.conf import default_settings
from gluepy.utils.loading import empty



class SettingsTestCase(TestCase):

    def setUp(self) -> None:
        # Ensure settings has not been evaluated
        # by other tests.
        default_settings._wrapped = empty
        return super().setUp()

    def test_settings_populated(self):
        # default_settings is not evaluated yet.
        self.assertEqual(default_settings._wrapped, empty)
        # When we try to access a setting, it is being populated by our ``settings.py``
        self.assertEqual(default_settings.STORAGE_BACKEND, "gluepy.files.storages.MemoryStorage")
        # It is now fully evaluated and no longer lazy.
        self.assertNotEqual(default_settings._wrapped, empty)

