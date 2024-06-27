import io
import os
from unittest import TestCase, mock
from gluepy.files.storages import GoogleStorage
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

    # def test_cp(self):
    #
    #     self.storage.isdir = mock.Mock()
    #     self.storage.isdir.return_value = False
    #     self.storage.exists = mock.Mock()
    #     self.storage.exists.side_effect = (False, True)
    #     with mock.patch("gluepy.files.storages.local.shutil.copy2") as mock_copy2:
    #         self.storage.cp("file.txt", "file2.txt")

    #     mock_copy2.assert_called_once_with(
    #         os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
    #         os.path.join(default_settings.STORAGE_ROOT, "file2.txt"),
    #         follow_symlinks=True,
    #     )

    # def test_cp_overwrite_error(self):
    #
    #     self.storage.isdir = mock.Mock()
    #     self.storage.isdir.return_value = False
    #     # Mock that file already exists
    #     self.storage.exists = mock.Mock()
    #     self.storage.exists.side_effect = (True, True)
    #     with self.assertRaises(FileExistsError):
    #         # overwrite=False raise error if file already exists.
    #         self.storage.cp("file.txt", "file2.txt", overwrite=False)

    # def test_cp_overwrite_success(self):
    #
    #     self.storage.isdir = mock.Mock()
    #     self.storage.isdir.return_value = False
    #     # Mock that file already exists
    #     self.storage.exists = mock.Mock()
    #     self.storage.exists.side_effect = (True, True)
    #     with mock.patch("gluepy.files.storages.local.shutil.copy2") as mock_copy2:
    #         # overwrite=True is necessary if file already exist
    #         self.storage.cp("file.txt", "file2.txt", overwrite=True)
    #     mock_copy2.assert_called_once_with(
    #         os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
    #         os.path.join(default_settings.STORAGE_ROOT, "file2.txt"),
    #         follow_symlinks=True,
    #     )

    # def test_ls(self):
    #
    #     with mock.patch("gluepy.files.storages.local.os.listdir") as mock_ls:
    #         mock_ls.return_value = ["file.txt", "file2.txt", "directory"]
    #         self.storage.isdir = mock.Mock()
    #         self.storage.isdir.side_effect = lambda x: x in {
    #             os.path.join(default_settings.STORAGE_ROOT, "directory")
    #         }
    #         self.storage.isfile = mock.Mock()
    #         self.storage.isfile.side_effect = lambda x: x in {
    #             os.path.join(default_settings.STORAGE_ROOT, "file.txt"),
    #             os.path.join(default_settings.STORAGE_ROOT, "file2.txt"),
    #         }
    #         files, dirs = self.storage.ls(".")
    #     self.assertEqual(files, ["file.txt", "file2.txt"])
    #     self.assertEqual(dirs, ["directory"])

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
