import os
from io import BytesIO
import pandas as pd
from unittest import TestCase, mock
from gluepy.files.data import PandasDataManager


class PandasDataManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.data_manager = PandasDataManager()
        return super().setUp()

    def test_read_csv(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_csv(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            mock_storage.runpath.return_value = "runs/2024/01/01/1234/file.csv"
            df = self.data_manager.read("file.csv")

        mock_storage.open.assert_called_once_with("runs/2024/01/01/1234/file.csv")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_read_csv_root(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_csv(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            df = self.data_manager.read("file.csv", root=True)

        mock_storage.open.assert_called_once_with("file.csv")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_read_parquet(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_parquet(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            mock_storage.runpath.return_value = "runs/2024/01/01/1234/file.parquet"
            df = self.data_manager.read("file.parquet")

        mock_storage.open.assert_called_once_with("runs/2024/01/01/1234/file.parquet")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_read_parquet_root(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_parquet(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            df = self.data_manager.read("file.parquet", root=True)

        mock_storage.open.assert_called_once_with("file.parquet")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_read_json(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_json(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            mock_storage.runpath.return_value = "runs/2024/01/01/1234/file.json"
            df = self.data_manager.read("file.json")

        mock_storage.open.assert_called_once_with("runs/2024/01/01/1234/file.json")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_read_json_root(self):
        # Prepare mock
        stream = BytesIO()
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        df_mock.to_json(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        # Test
        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.open.return_value = stream.read()
            df = self.data_manager.read("file.json", root=True)

        mock_storage.open.assert_called_once_with("file.json")
        pd.testing.assert_frame_equal(df, df_mock)

    def test_write_csv(self):
        stream = BytesIO()
        df = pd.DataFrame({"col": [1, 2, 3]})
        df.to_csv(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.runpath.return_value = "runs/2024/01/01/1234/file.csv"
            self.data_manager.write("file.csv", df, index=False)
            mock_storage.touch.assert_called_once()
            file_path = mock_storage.touch.call_args[1]["file_path"]
            content = mock_storage.touch.call_args[1]["content"]

        self.assertEqual(file_path, "runs/2024/01/01/1234/file.csv")
        self.assertEqual(content.read(), stream.read())

    def test_write_csv_root(self):
        stream = BytesIO()
        df = pd.DataFrame({"col": [1, 2, 3]})
        df.to_csv(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            self.data_manager.write("file.csv", df, root=True, index=False)
            mock_storage.touch.assert_called_once()
            file_path = mock_storage.touch.call_args[1]["file_path"]
            content = mock_storage.touch.call_args[1]["content"]

        self.assertEqual(file_path, "file.csv")
        self.assertEqual(content.read(), stream.read())

    def test_write_parquet(self):
        stream = BytesIO()
        df = pd.DataFrame({"col": [1, 2, 3]})
        df.to_parquet(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            mock_storage.runpath.return_value = "runs/2024/01/01/1234/file.parquet"
            self.data_manager.write("file.parquet", df, index=False)
            mock_storage.touch.assert_called_once()
            file_path = mock_storage.touch.call_args[1]["file_path"]
            content = mock_storage.touch.call_args[1]["content"]

        self.assertEqual(file_path, "runs/2024/01/01/1234/file.parquet")
        self.assertEqual(content.read(), stream.read())

    def test_write_parquet_root(self):
        stream = BytesIO()
        df = pd.DataFrame({"col": [1, 2, 3]})
        df.to_parquet(stream, index=False)
        stream.seek(0, os.SEEK_SET)

        with mock.patch("gluepy.files.data.pandas.default_storage") as mock_storage:
            self.data_manager.write("file.parquet", df, root=True, index=False)
            mock_storage.touch.assert_called_once()
            file_path = mock_storage.touch.call_args[1]["file_path"]
            content = mock_storage.touch.call_args[1]["content"]

        self.assertEqual(file_path, "file.parquet")
        self.assertEqual(content.read(), stream.read())

    def test_read_sql(self):
        df_mock = pd.DataFrame({"col": [1, 2, 3]})
        with mock.patch.dict("sys.modules", {"pandas_gbq": mock.Mock()}) as _:
            import sys

            mock_gbq = sys.modules["pandas_gbq"]
            mock_gbq.read_gbq.return_value = df_mock
            with mock.patch(
                "gluepy.files.data.pandas.default_settings"
            ) as mock_settings:
                mock_settings.GCP_PROJECT_ID = "test-project"
                df = self.data_manager.read_sql("SELECT * FROM table")
            mock_gbq.read_gbq.assert_called_once_with(
                "SELECT * FROM table",
                project_id="test-project",
                use_bqstorage_api=True,
            )
            pd.testing.assert_frame_equal(df, df_mock)

    def test_read_sql_import_error(self):
        with mock.patch.dict("sys.modules", {"pandas_gbq": None}):
            with self.assertRaises(ImportError):
                self.data_manager.read_sql("SELECT * FROM table")

    def test_read_unsupported_extension(self):
        with self.assertRaises(ValueError):
            with mock.patch("gluepy.files.data.pandas.default_storage"):
                self.data_manager.read("file.xyz")

    def test_write_unsupported_extension(self):
        df = pd.DataFrame({"col": [1, 2, 3]})
        with self.assertRaises(ValueError):
            with mock.patch("gluepy.files.data.pandas.default_storage"):
                self.data_manager.write("file.xyz", df)
