import io
import os
from unittest import TestCase, mock
from gluepy.files.storages import LocalStorage
from gluepy.conf import default_settings


class LocalStorageTestCase(TestCase):

    def test_touch(self):
        storage = LocalStorage()
        with mock.patch("builtins.open") as mock_file:
            storage.touch("file.txt", io.StringIO("foo"))
        
        mock_file.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
            mode="wb"
        )

    def test_cp(self):
        storage = LocalStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        storage.exists = mock.Mock()
        storage.exists.side_effect = (False, True)
        with mock.patch("gluepy.files.storages.local.shutil.copy2") as mock_copy2:
            storage.cp("file.txt", "file2.txt")
        
        mock_copy2.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
            os.path.join(default_settings.STORAGE_ROOT, "file2.txt"),
            follow_symlinks=True
        )

    def test_cp_overwrite_error(self):
        storage = LocalStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        # Mock that file already exists
        storage.exists = mock.Mock()
        storage.exists.side_effect = (True, True)
        with self.assertRaises(FileExistsError):
            # overwrite=False raise error if file already exists.
            storage.cp("file.txt", "file2.txt", overwrite=False)

    def test_cp_overwrite_success(self):
        storage = LocalStorage()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        # Mock that file already exists
        storage.exists = mock.Mock()
        storage.exists.side_effect = (True, True)
        with mock.patch("gluepy.files.storages.local.shutil.copy2") as mock_copy2:
            # overwrite=True is necessary if file already exist
            storage.cp("file.txt", "file2.txt", overwrite=True)
        
        mock_copy2.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
            os.path.join(default_settings.STORAGE_ROOT, "file2.txt"),
            follow_symlinks=True
        )

    def test_open(self):
        storage = LocalStorage()
        with mock.patch("builtins.open", mock.mock_open(read_data="foo")) as mock_file:
            f = storage.open("file.txt")
        
        mock_file.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
            mode="rb"
        )
        # The returned value from f is the contents of the file,
        # not a stream.
        self.assertEqual(f, "foo")

    def test_ls(self):
        storage = LocalStorage()
        with mock.patch("gluepy.files.storages.local.os.listdir") as mock_ls:
            mock_ls.return_value = [
                "file.txt", "file2.txt", "directory"
            ]
            storage.isdir = mock.Mock()
            storage.isdir.side_effect = lambda x: x in {os.path.join(default_settings.STORAGE_ROOT, "directory")}
            storage.isfile = mock.Mock()
            storage.isfile.side_effect = lambda x: x in {os.path.join(default_settings.STORAGE_ROOT, "file.txt"), os.path.join(default_settings.STORAGE_ROOT, "file2.txt")}
            files, dirs = storage.ls(".")
        
        self.assertEqual(files, ["file.txt", "file2.txt"])
        self.assertEqual(dirs, ["directory"])

    def test_mkdir(self):
        storage = LocalStorage()
        with mock.patch("gluepy.files.storages.local.os.makedirs") as mock_makedirs:
            storage.exists = mock.Mock()
            storage.exists.return_value = True
            storage.mkdir("path/to/dir")

        mock_makedirs.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "path", "to", "dir"),
            exist_ok=True
        )

    def test_isdir(self):
        storage = LocalStorage()
        with mock.patch("gluepy.files.storages.local.os.path.isdir") as mock_isdir:
            storage.exists = mock.Mock()
            storage.exists.return_value = True
            self.assertTrue(storage.isdir("path/to/dir"))

        mock_isdir.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "path", "to", "dir"),
        )

    def test_isfile(self):
        storage = LocalStorage()
        with mock.patch("gluepy.files.storages.local.os.path.isfile") as mock_isfile:
            storage.exists = mock.Mock()
            storage.exists.return_value = True
            self.assertTrue(storage.isfile("path/to/dir/file.txt"))

        mock_isfile.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "path", "to", "dir", "file.txt"),
        )

    def test_exists(self):
        storage = LocalStorage()
        with mock.patch("gluepy.files.storages.local.os.path.exists") as mock_exists:
            storage.exists("path/to/dir")

        mock_exists.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "path", "to", "dir"),
        )
