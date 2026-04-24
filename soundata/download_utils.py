"""utilities for downloading from the web."""

import glob
import logging
import os
import shutil
import tarfile
import urllib.request
import zipfile
import subprocess
import py7zr
from tqdm import tqdm

from soundata.validate import md5

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class RemoteFileMetadata(object):
    """The metadata for a remote file

    Attributes:
        filename (str): the remote file's basename
        url (str): the remote file's url
        checksum (str): the remote file's md5 checksum
        destination_dir (str or None): the relative path for where to save the file
        unpack_directories (list or None): list of relative directories. For each directory
            the contents will be moved to destination_dir (or data_home if not provided)

    """

    def __init__(
        self, filename, url, checksum, destination_dir=None, unpack_directories=None
    ):
        raise NotImplementedError


def downloader(
    save_dir,
    remotes=None,
    index=None,
    partial_download=None,
    info_message=None,
    force_overwrite=False,
    cleanup=False,
):
    """Download data to `save_dir` and optionally log a message

    Args:
        save_dir (str):
            The directory to download the data
        remotes (dict or None):
            A dictionary of RemoteFileMetadata tuples of data in zip format.
            If an element of the dictionary is a list of RemoteFileMetadata, it is handled as a multipart zip file
            If None, there is no data to download
        index (core.Index):
            A soundata Index class, which contains a remote index to be downloaded
            or a subset of remotes to download by default.
        partial_download (list or None):
            A list of keys to partially download the remote objects of the download dict.
            If None, all data specified by the index is downloaded
        info_message (str or None):
            A string of info to log when this function is called.
            If None, no string is logged.
        force_overwrite (bool):
            If True, existing files are overwritten by the downloaded files.
        cleanup (bool):
            Whether to delete the zip/tar file after extracting.
    """
    pass


class DownloadProgressBar(tqdm):
    """Wrap tqdm to show download progress"""

    def update_to(self, b=1, bsize=1, tsize=None):
        pass


def download_multipart_zip(zip_remotes, save_dir, force_overwrite, cleanup):
    """Download and unzip a multipart zip file.

    Args:
        zip_remotes (list):
            A list of RemoteFileMetadata Objects
            containing download information
        save_dir (str):
            Path to save downloaded file
        force_overwrite (bool):
            If True, overwrites existing files
        cleanup (bool):
            If True, remove zipfile after unziping

    """
    pass


def download_from_remote(remote, save_dir, force_overwrite):
    """Download a remote dataset into path

    Fetch a dataset pointed by remote's url, save into path using remote's
    filename and ensure its integrity based on the MD5 Checksum of the
    downloaded file.

    Adapted from scikit-learn's sklearn.datasets.base._fetch_remote.

    Args:
        remote (RemoteFileMetadata): Named tuple containing remote dataset
            meta information: url, filename and checksum
        save_dir (str): Directory to save the file to. Usually `data_home`
        force_overwrite  (bool):
            If True, overwrite existing file with the downloaded file.
            If False, does not overwrite, but checks that checksum is consistent.

    Returns:
        str: Full path of the created file.

    """
    pass


def download_zip_file(zip_remote, save_dir, force_overwrite, cleanup):
    """Download and unzip a zip file.

    Args:
        zip_remote (RemoteFileMetadata):
            Object containing download information
        save_dir (str):
            Path to save downloaded file
        force_overwrite (bool):
            If True, overwrites existing files
        cleanup (bool):
            If True, remove zipfile after unziping

    """
    pass


def extractall_unicode(zfile, out_dir):
    """Extract all files inside a zip archive to a output directory.

    In comparison to the zipfile, it checks for correct file name encoding

    Args:
        zfile (obj): Zip file object created with zipfile.ZipFile
        out_dir (str): Output folder

    """
    pass


def unzip(zip_path, cleanup):
    """Unzip a zip file inside it's current directory.

    Args:
        zip_path (str): Path to zip file
        cleanup (bool): If True, remove zipfile after unzipping

    """
    pass


def download_7z_file(tar_remote, save_dir, force_overwrite, cleanup):
    """Download and untar a tar file.

    Args:
        tar_remote (RemoteFileMetadata): Object containing download information
        save_dir (str): Path to save downloaded file
        force_overwrite (bool): If True, overwrites existing files
        cleanup (bool): If True, remove tarfile after untarring

    """
    pass


def un7z(sevenz_path, cleanup):
    """Unzip a 7z file inside its current directory.

    Args:
        sevenz_path (str): Path to the 7z file
        cleanup (bool): If True, remove 7z file after extraction

    """
    pass


def download_tar_file(tar_remote, save_dir, force_overwrite, cleanup):
    """Download and untar a tar file.

    Args:
        tar_remote (RemoteFileMetadata): Object containing download information
        save_dir (str): Path to save downloaded file
        force_overwrite (bool): If True, overwrites existing files
        cleanup (bool): If True, remove tarfile after untarring

    """
    pass


def untar(tar_path, cleanup):
    """Untar a tar file inside it's current directory.

    Args:
        tar_path (str): Path to tar file
        cleanup (bool): If True, remove tarfile after untarring

    """
    pass


def move_directory_contents(source_dir, target_dir):
    """Move the contents of source_dir into target_dir, and delete source_dir

    Args:
        source_dir (str): path to source directory
        target_dir (str): path to target directory

    """
    pass
