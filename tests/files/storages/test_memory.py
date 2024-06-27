import io
import os
from unittest import TestCase, mock
from gluepy.files.storages.memory import MemoryStorage
from gluepy.conf import default_settings


class MemoryStorageTestCase(TestCase):
    def test_touch(self):
        contents = io.StringIO("foo")
        storage = MemoryStorage()
        storage.touch("file.txt", contents)

        full_path = os.path.join(default_settings.STORAGE_ROOT, "file.txt")
        paths = os.path.dirname(full_path).split(storage.separator)
        dir = storage.FILE_SYSTEM
        for path in paths:
            dir = dir[path]
        self.assertEqual(dir["file.txt"], contents)

    def test_cp(self):
        storage = MemoryStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        storage.exists = mock.Mock()
        storage.exists.return_value = False
        storage.open = mock.Mock()
        storage.open.return_value = "Foo"

        storage.cp("file.txt", "file2.txt")

        full_path = os.path.join(default_settings.STORAGE_ROOT, "file2.txt")
        paths = os.path.dirname(full_path).split(storage.separator)
        dir = storage.FILE_SYSTEM
        for path in paths:
            dir = dir[path]
        self.assertEqual(
            dir["file2.txt"].read(),
            "Foo",
        )

    def test_cp_overwrite_error(self):
        storage = MemoryStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        # Mock that file already exists
        storage.exists = mock.Mock()
        storage.exists.side_effect = (True, True)
        with self.assertRaises(FileExistsError):
            # overwrite=False raise error if file already exists.
            storage.cp("file.txt", "file2.txt", overwrite=False)

    def test_cp_overwrite_success(self):
        storage = MemoryStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        storage.exists = mock.Mock()
        storage.exists.return_value = True
        storage.open = mock.Mock()
        storage.open.return_value = "Foo"

        storage.cp("file.txt", "file2.txt", overwrite=True)

        full_path = os.path.join(default_settings.STORAGE_ROOT, "file2.txt")
        paths = os.path.dirname(full_path).split(storage.separator)
        dir = storage.FILE_SYSTEM
        for path in paths:
            dir = dir[path]
        self.assertEqual(
            dir["file2.txt"].read(),
            "Foo",
        )

    def test_open(self):
        storage = MemoryStorage()
        storage.touch("path/file.txt", io.StringIO("foo"))
        f = storage.open("path/file.txt")
        # The returned value from f is the contents of the file,
        # not a stream.
        self.assertEqual(f, "foo")

    def test_rm(self):
        storage = MemoryStorage()
        storage.touch("file.txt", io.StringIO("foo"))
        self.assertTrue(storage.exists("file.txt"))
        storage.rm("file.txt")
        self.assertFalse(storage.exists("file.txt"))

    def test_rm_recursive_error(self):
        storage = MemoryStorage()
        storage.touch("path/file.txt", io.StringIO("foo"))
        self.assertTrue(storage.exists("path/file.txt"))
        with self.assertRaises(ValueError):
            storage.rm("path/", recursive=False)

    def test_rm_recursive_success(self):
        storage = MemoryStorage()
        storage.touch("path/file.txt", io.StringIO("foo"))
        self.assertTrue(storage.exists("path/file.txt"))
        storage.rm("path/", recursive=True)
        self.assertFalse(storage.exists("file.txt"))

    def test_ls(self):
        storage = MemoryStorage()

        storage.touch("path/file.txt", io.StringIO("foo"))
        storage.touch("path/file2.txt", io.StringIO("foo"))
        storage.touch("path/directory/file3.txt", io.StringIO("foo"))

        files, dirs = storage.ls("path/")

        self.assertEqual(files, ["file.txt", "file2.txt"])
        self.assertEqual(dirs, ["directory"])

    def test_mkdir(self):
        storage = MemoryStorage()
        storage.mkdir("path/to/dir")
        self.assertTrue(storage.exists("path/to/dir"))

    def test_isdir(self):
        storage = MemoryStorage()
        storage.touch("path/to/dir/file.txt", io.StringIO("foo"))
        self.assertTrue(storage.isdir("path/to/dir"))
        self.assertFalse(storage.isdir("path/to/dir/file.txt"))

    def test_isfile(self):
        storage = MemoryStorage()
        storage.touch("path/to/dir/file.txt", io.StringIO("foo"))
        self.assertTrue(storage.isfile("path/to/dir/file.txt"))
        self.assertFalse(storage.isfile("path/to/dir"))

    def test_exists(self):
        storage = MemoryStorage()
        storage.touch("path/to/dir/file.txt", io.StringIO("foo"))
        self.assertTrue(storage.exists("path/to/dir"))
        self.assertTrue(storage.exists("path/to/dir/file.txt"))
        self.assertFalse(storage.exists("path/to/missing-dir"))
