"""Core soundata classes"""

import json
import os
import sys
import random
import types
from typing import Any, List, Optional

import numpy as np

from soundata import download_utils
from soundata import validate

MAX_STR_LEN = 100
DOCS_URL = "https://soundata.readthedocs.io/en/stable/source/soundata.html"
DISCLAIMER = """
******************************************************************************************
DISCLAIMER: soundata is a software package with its own license which is independent from
this dataset's license. We don not take responsibility for possible inaccuracies in the
license information provided in soundata. It is the user's responsibility to be informed
and respect the dataset's license.
******************************************************************************************
"""

##### decorators ######


class cached_property(object):
    """Cached property decorator

    A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the
    property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76

    """

    def __init__(self, func):
        raise NotImplementedError

    def __get__(self, obj: Any, cls: type) -> Any:
        raise NotImplementedError


def docstring_inherit(parent):
    """Decorator function to inherit docstrings from the parent class.

    Adds documented Attributes from the parent to the child docs.

    """
    raise NotImplementedError


def copy_docs(original):
    """
    Decorator function to copy docs from one function to another
    """
    raise NotImplementedError


##### Core Classes #####


class Dataset(object):
    """soundata Dataset class

    Attributes:
        data_home (str): path where soundata will look for the dataset
        version (str): dataset version
        name (str): the identifier of the dataset
        bibtex (str or None): dataset citation/s in bibtex format
        indexes (dict or None): indexes to be downloaded
        remotes (dict or None): data to be downloaded
        readme (str): information about the dataset
        clip (function): a function mapping a clip_id to a soundata.core.Clip
        clipgroup (function): a function mapping a clipgroup_id to a soundata.core.Clipgroup

    """

    def __init__(
        self,
        data_home=None,
        version="default",
        name=None,
        clip_class=None,
        clipgroup_class=None,
        bibtex=None,
        indexes=None,
        remotes=None,
        download_info=None,
        license_info=None,
    ):
        """Dataset init method

        Args:
            data_home (str or None): path where soundata will look for the dataset
            version (str): dataset version
            name (str or None): the identifier of the dataset
            clip_class (soundata.core.Clip or None): a Clip class
            clipgroup_class (soundata.core.Clipgroup or None): a Clipgroup class
            bibtex (str or None): dataset citation/s in bibtex format
            remotes (dict or None): data to be downloaded
            download_info (str or None): download instructions or caveats
            license_info (str or None): license of the dataset

        """
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    @cached_property
    def _index(self):
        pass

    @cached_property
    def _metadata(self):
        pass

    @property
    def default_path(self):
        """Get the default path for the dataset

        Returns:
            str: Local path to the dataset

        """
        pass

    def _clip(self, clip_id):
        """Load a clip by clip_id.

        Hidden helper function that gets called as a lambda.

        Args:
            clip_id (str): clip id of the clip

        Returns:
           Clip: a Clip object

        """
        pass

    def _clipgroup(self, clipgroup_id):
        """Load a clipgroup by clipgroup_id.

        Hidden helper function that gets called as a lambda.

        Args:
            clipgroup_id (str): clipgroup id of the clipgroup

        Returns:
            ClipGroup: an instance of this dataset's ClipGroup object

        """
        pass

    def load_clips(self):
        """Load all clips in the dataset

        Returns:
            dict:
                {`clip_id`: clip data}

        Raises:
            NotImplementedError: If the dataset does not support Clips

        """
        pass

    def load_clipgroups(self):
        """Load all clipgroups in the dataset

        Returns:
            dict:
                {`clipgroup_id`: clipgroup data}

        Raises:
            NotImplementedError: If the dataset does not support Clipgroups

        """
        pass

    def choice_clip(self):
        """Choose a random clip

        Returns:
            Clip: a Clip object instantiated by a random clip_id

        """
        pass

    def choice_clipgroup(self):
        """Choose a random clipgroup

        Returns:
            Clipgroup: a Clipgroup object instantiated by a random clipgroup_id

        """
        pass

    def cite(self):
        """
        Print the reference
        """
        pass

    def license(self):
        """
        Print the license
        """
        pass

    def download(self, partial_download=None, force_overwrite=False, cleanup=False):
        """Download data to `save_dir` and optionally print a message.

        Args:
            partial_download (list or None):
                A list of keys of remotes to partially download.
                If None, all data is downloaded
            force_overwrite (bool):
                If True, existing files are overwritten by the downloaded files.
            cleanup (bool):
                Whether to delete any zip/tar files after extracting.

        Raises:
            ValueError: if invalid keys are passed to partial_download
            IOError: if a downloaded file's checksum is different from expected

        """
        pass

    def explore_dataset(self, clip_id=None):  # pragma: no cover
        """Explore the dataset for a given clip_id or a random clip if clip_id is None.

        Args:
            clip_id (str or None):
                The identifier of the clip to explore. If None, a random clip will be chosen.

        """
        pass

    @cached_property
    def clip_ids(self):
        """Return clip ids

        Returns:
            list: A list of clip ids

        """
        pass

    @cached_property
    def clipgroup_ids(self):
        """Return clip ids

        Returns:
            list: A list of clip ids

        """
        pass

    def validate(self, verbose=True):
        """Validate if the stored dataset is a valid version

        Args:
            verbose (bool): If False, don't print output

        Returns:
            * list - files in the index but are missing locally
            * list - files which have an invalid checksum

        """
        pass


class Clip(object):
    """Clip base class

    See the docs for each dataset loader's Clip class for details

    """

    def __init__(self, clip_id, data_home, dataset_name, index, metadata):
        """Clip init method. Sets boilerplate attributes, including:

        - ``clip_id``
        - ``_dataset_name``
        - ``_data_home``
        - ``_clip_paths``
        - ``_clip_metadata``

        Args:
            clip_id (str): clip id
            data_home (str): path where soundata will look for the dataset
            dataset_name (str): the identifier of the dataset
            index (dict): the dataset's file index
            metadata (function or None): a function returning a dictionary of metadata or None

        """
        raise NotImplementedError

    @property
    def _clip_metadata(self):
        pass

    def __repr__(self):
        raise NotImplementedError

    def get_path(self, key):
        """Get absolute path to clip audio and annotations. Returns None if
        the path in the index is None

        Args:
            key (string): Index key of the audio or annotation type

        Returns:
            str or None: joined path string or None

        """
        pass


class ClipGroup(Clip):
    """ClipGroup class.

    A clipgroup class is a collection of clip objects and their associated audio
    that can be mixed together.
    A clipgroup is itself a Clip, and can have its own associated audio (such as
    a mastered mix), its own metadata and its own annotations.

    """

    def __init__(
        self, clipgroup_id, data_home, dataset_name, index, clip_class, metadata
    ):
        """Clipgroup init method. Sets boilerplate attributes, including:

        - ``clipgroup_id``
        - ``_dataset_name``
        - ``_data_home``
        - ``_clipgroup_paths``
        - ``_clipgroup_metadata``

        Args:
            clipgroup_id (str): clipgroup id
            data_home (str): path where soundata will look for the dataset
            dataset_name (str): the identifier of the dataset
            index (dict): the dataset's file index
            metadata (function or None): a function returning a dictionary of metadata or None

        """
        raise NotImplementedError

    @property
    def clips(self):
        pass

    @property
    def clip_audio_property(self):
        """The clip's audio property.

        Returns:

        """
        raise NotImplementedError("Mixing is not supported for this dataset")

    @property
    def _clipgroup_metadata(self):
        pass

    def get_path(self, key):
        """Get absolute path to clipgroup audio and annotations. Returns None if
        the path in the index is None

        Args:
            key (string): Index key of the audio or annotation type

        Returns:
            str or None: joined path string or None

        """
        pass

    def get_target(self, clip_keys, weights=None, average=True, enforce_length=True):
        """Get target which is a linear mixture of clips

        Args:
            clip_keys (list): list of clip keys to mix together
            weights (list or None): list of positive scalars to be used in the average
            average (bool): if True, computes a weighted average of the clips
                if False, computes a weighted sum of the clips
            enforce_length (bool): If True, raises ValueError if the clips are
                not the same length. If False, pads audio with zeros to match the length
                of the longest clip

        Returns:
            np.ndarray: target audio with shape (n_channels, n_samples)

        Raises:
            ValueError:
                if sample rates of the clips are not equal
                if enforce_length=True and lengths are not equal

        """
        pass

    def get_random_target(self, n_clips=None, min_weight=0.3, max_weight=1.0):
        """Get a random target by combining a random selection of clips with random weights

        Args:
            n_clips (int or None): number of clips to randomly mix. If None, uses all clips
            min_weight (float): minimum possible weight when mixing
            max_weight (float): maximum possible weight when mixing

        Returns:
            * np.ndarray - mixture audio with shape (n_samples, n_channels)
            * list - list of keys of included clips
            * list - list of weights used to mix clips

        """
        pass

    def get_mix(self):
        """Create a linear mixture given a subset of clips.

        Args:
            clip_keys (list): list of clip keys to mix together

        Returns:
            np.ndarray: mixture audio with shape (n_samples, n_channels)

        """
        pass


class Index(object):
    """Class for storing information about dataset indexes.

    Args:
        filename (str): The index filename (not path), e.g. "example_dataset_index_1.2.json"
        url (str or None): None if index is not remote, or a url to download from
        checksum (str or None): None if index is not remote, or the md5 checksum of the file
        partial_download (list or None): if provided, specifies a subset of Dataset.remotes
            corresponding to this index to be downloaded. If None, all Dataset.remotes will
            be downloaded when calling Dataset.download()

    Attributes:
        remote (download_utils.RemoteFileMetadata or None): None if index is not remote, or
            a RemoteFileMetadata object
        partial_download (list or None): a list of keys to partially download, or None

    """

    def __init__(
        self,
        filename: str,
        url: Optional[str] = None,
        checksum: Optional[str] = None,
        partial_download: Optional[List[str]] = None,
    ):
        raise NotImplementedError

    def get_path(self) -> str:
        """Get the absolute path to the index file

        Returns:
            str: absolute path to the index file
        """
        pass
