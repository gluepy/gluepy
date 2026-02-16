import io
import os
from unittest import TestCase, mock
from gluepy.files.storages.google import GoogleStorage
from gluepy.conf import default_settings


class GoogleStorageTestCase(TestCase):
    def setUp(self) -> None:
        with mock.patch("gluepy.files.storages.google.storage.Client") as _:
            self.storage = GoogleStorage()
            self.storage.bucket = mock.Mock()
            self.storage.client = mock.Mock()
        return super().setUp()

    def test_touch(self):
        content = io.BytesIO(b"foo")
        mock_blob = mock.Mock()
        mock_retry_instance = mock.Mock()
        self.storage.bucket.blob.return_value = mock_blob
        with mock.patch("gluepy.files.storages.google.retry.Retry") as mock_retry:
            mock_retry.return_value = mock_retry_instance
            self.storage.touch("file.txt", content)
            self.storage.bucket.blob.assert_called_once_with(
                os.path.join(default_settings.STORAGE_ROOT, "file.txt")
            )
            mock_blob.upload_from_file.assert_called_once_with(
                content, rewind=True, retry=mock_retry_instance, size=len(b"foo")
            )

    def test_open(self):
        mock_blob = mock.Mock()
        mock_bytesio_instance = mock.Mock()
        mock_bytesio_instance.read.return_value = "foo"
        self.storage.bucket.blob.return_value = mock_blob
        with mock.patch("gluepy.files.storages.google.BytesIO") as mock_bytesio:
            mock_bytesio.return_value = mock_bytesio_instance
            f = self.storage.open("file.txt")
        self.storage.bucket.blob.assert_called_once_with(
            os.path.join(default_settings.STORAGE_ROOT, "file.txt")
        )
        mock_blob.download_to_file.assert_called_once_with(mock_bytesio_instance)
        # The returned value from f is the contents of the file,
        # not a stream.
        self.assertEqual(f, "foo")

    def test_cp(self):
        with mock.patch("gluepy.files.storages.google.storage.Client") as _:
            storage = GoogleStorage()
            storage.bucket = mock.Mock()
            storage.client = mock.Mock()
        storage.isdir = mock.Mock()
        storage.isdir.return_value = False
        storage.isfile = mock.Mock()
        storage.isfile.return_value = True
        storage.exists = mock.Mock()
        storage.exists.side_effect = (True, False)
        storage.open = mock.Mock()
        storage.open.return_value = "Foo"
        storage.touch = mock.Mock()
        with mock.patch("gluepy.files.storages.local.shutil.copy2") as _:
            storage.cp("file.txt", "file2.txt")

        storage.open.assert_called_once_with("file.txt")
        storage.touch.assert_called_once()

    def test_ls(self):
        mock_blob_a = mock.Mock()
        mock_blob_a.name = os.path.join(default_settings.STORAGE_ROOT, "file.txt")
        mock_blob_a.exists.side_effect = (False,)
        mock_blob_b = mock.Mock()
        mock_blob_b.name = os.path.join(default_settings.STORAGE_ROOT, "file2.txt")
        mock_blob_b.exists.side_effect = (False,)
        mock_blob_c = mock.Mock()
        mock_blob_c.name = os.path.join(default_settings.STORAGE_ROOT, "directory")
        mock_blob_c.exists.side_effect = (True,)
        self.storage.bucket.blob.side_effect = (mock_blob_a, mock_blob_b, mock_blob_c)
        self.storage.client.list_blobs.side_effect = (
            # Blobs returned as part of .ls() call
            [mock_blob_a, mock_blob_b, mock_blob_c],
            [],
            [],
            # Blob returned when running isdir on final iteration
            [mock_blob_c],
        )
        files, dirs = self.storage.ls(".")
        self.assertEqual(files, ["file.txt", "file2.txt"])
        self.assertEqual(dirs, ["directory/"])

    def test_mkdir(self):
        mock_blob = mock.Mock()
        mock_blob.exists.side_effect = (False, False, True)
        self.storage.bucket.blob.return_value = mock_blob
        self.storage.client.list_blobs.return_value = []
        self.storage.mkdir("path/to/dir")
        mock_blob.upload_from_file.assert_called_once()

    def test_isdir(self):
        mock_blob = mock.Mock()
        mock_blob.exists.side_effect = (True, False, False)
        self.storage.bucket.blob.return_value = mock_blob
        self.storage.client.list_blobs.side_effect = ([], ["file.txt"], [])
        self.assertTrue(self.storage.isdir("path/to/dir"))
        self.storage.client.list_blobs.assert_called_once_with(
            self.storage.bucket,
            prefix=(
                os.path.join(default_settings.STORAGE_ROOT, "path", "to", "dir") + "/"
            ),
            max_results=1,
        )
        self.assertTrue(self.storage.isdir("path/to/dir"))
        self.assertFalse(self.storage.isdir("path/to/dir"))

    def test_isfile(self):
        mock_blob = mock.Mock()
        mock_blob.exists.return_value = True
        self.storage.bucket.blob.return_value = mock_blob
        self.assertTrue(self.storage.isfile("path/to/dir/file.txt"))
        self.assertFalse(self.storage.isfile("path/to/dir/"))

    def test_exists(self):
        mock_blob = mock.Mock()
        mock_blob.exists.return_value = True
        self.storage.bucket.blob.return_value = mock_blob
        self.storage.client.list_blobs.return_value = []
        self.assertTrue(self.storage.exists("path/to/dir"))

    def test_exists_missing(self):
        mock_blob = mock.Mock()
        mock_blob.exists.return_value = False
        self.storage.bucket.blob.return_value = mock_blob
        self.storage.client.list_blobs.return_value = []
        self.assertFalse(self.storage.exists("path/to/dir"))

    def test_rm_file(self):
        mock_blob = mock.Mock()
        self.storage.bucket.blob.return_value = mock_blob
        # Mock isdir to return False (it's a file, not a directory)
        self.storage.isdir = mock.Mock(return_value=False)
        self.storage.rm("file.txt")
        mock_blob.delete.assert_called_once()

    def test_rm_recursive(self):
        mock_blob = mock.Mock()
        # isdir checks: first call for "path/" -> True (it's a dir)
        mock_blob.exists.side_effect = [False, True, True]
        self.storage.bucket.blob.return_value = mock_blob

        mock_child_blob = mock.Mock()
        mock_child_blob.name = os.path.join(
            default_settings.STORAGE_ROOT, "path", "child.txt"
        )
        mock_child_blob.exists.return_value = False

        # list_blobs calls: ls for "path/" returns child, then isdir checks
        self.storage.client.list_blobs.side_effect = [
            [mock_child_blob],  # isdir check for "path/"
            [mock_child_blob],  # ls call
            [],  # isdir check for child blob
        ]

        # Mock isdir and ls to simplify
        self.storage.isdir = mock.Mock(side_effect=[True, False])
        self.storage.ls = mock.Mock(return_value=(["child.txt"], []))

        self.storage.rm("path/", recursive=True)
        mock_blob.delete.assert_called_once()

    def test_touch_stringio(self):
        content = io.StringIO("foo")
        mock_blob = mock.Mock()
        mock_retry_instance = mock.Mock()
        self.storage.bucket.blob.return_value = mock_blob
        with mock.patch("gluepy.files.storages.google.retry.Retry") as mock_retry:
            mock_retry.return_value = mock_retry_instance
            self.storage.touch("file.txt", content)
            # Verify upload_from_file was called (StringIO should be converted to BytesIO)
            mock_blob.upload_from_file.assert_called_once()
