from typing import Union
from io import StringIO, BytesIO
from .base import BaseStorage


class GoogleStorage(BaseStorage):
    """ "
    Storage support for Google Cloud Storage.
    """

    def __init__(self) -> None:
        super().__init__()
        self.client = ()

    def touch(self, file_path: str, content: Union[StringIO, BytesIO]) -> None:
        """Create a new blob at file path.

        Args:
            file_path (str): Path to file we want to create
            content (Union[StringIO, BytesIO]): Content of file we want to generate

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        raise NotImplementedError()

    def open(self, file_path: str, mode: str = "rb") -> Union[str, bytes]:
        """Opens a blob at file_path

        Args:
            file_path (str): File path of blob we want to open

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        raise NotImplementedError()

    def rm(self, path: str) -> None:
        """Delete a file

        Args:
            path (str): Path to file to delete

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        raise NotImplementedError()

    def cp(self, src_path: str, dest_path: str) -> None:
        """Copy a file from source to destination

        Args:
            src_path (str): Path to file or directory to copy.
            dest_path (str): Path to file or directory to copy to.
        """
        raise NotImplementedError()

    def ls(self, path: str) -> tuple[list[str], list[str]]:
        """List all files and directories at given path.

        Args:
            path (str): Path where we want to list contents of

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            Tuple[List[str], List[str]]:
              First list is files, second list is directories.
        """
        raise NotImplementedError()

    def mkdir(self, path: str, make_parents: bool = False) -> None:
        """Make a new directory at location

        Args:
            path (str): Path of directory we want to create
            make_parents (bool, optional): If we should generate parents
              folders as well. Defaults to False.

        Raises:
            NotImplementedError: Base class raise NotImplementedError
        """
        raise NotImplementedError()

    def isdir(self, path: str) -> bool:
        """Check if path is directory or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is directory or not
        """
        raise NotImplementedError()

    def isfile(self, path: str) -> bool:
        """Check if path is a file or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is file or not.
        """
        raise NotImplementedError()

    def exists(self, path: str) -> bool:
        """Check if path exists or not.

        Args:
            path (str): Path we want to check

        Raises:
            NotImplementedError: Base class raise NotImplementedError

        Returns:
            bool: True/False if path is file or not.
        """
        raise NotImplementedError()
