"""TAU NIGENS SSE 2021 Dataset Loader

.. admonition:: Dataset Info
    :class: dropdown

    **TAU NIGENS Spatial Sound Events: scene recordings with (moving) sound events of distinct categories**

    *Created By:*

        | Archontis Politis, Sharath Adavanne, Tuomas Virtanen.
        | Audio Research Group, Tampere University (Finland).

    Version 1.2.0

    *Description:*
        Spatial sound-scene recordings, consisting of sound events of distinct categories
        in a variety of acoustical spaces, and from multiple source directions and distances.
        The spatialization of all sound events is based on filtering through real spatial
        room impulse responses (RIRs) of diverse acoustic environments. The sound events are
        spatialized as either stationary sound sources, or moving sound sources, in which case
        time-variant RIRs are used.

        Each scene recording is delivered in microphone array (MIC) and first-order Ambisonics (FOA)
        format.

    *Audio Files Included:*
        * 600 one-minute-long sound scene recordings with annotations (development dataset).
        * 200 one-minute-long sound scene recordings without annotations (evaluation dataset).
        * Sampling rate is 24 kHz (16-bit signed integer PCM).
        * About 500 sound event samples distirbuted over 12 target classes.
        * About 400 sound event samples used as interference events.
        * 1st order HOA or tetrahedral microphone array formats.
        * Realistic spatialization and reverberation through multichannel RIRs collected in 13 different enclosures.
        * From 1184 to 6480 possible RIR positions across the different rooms.
        * Both static reverberant and moving reverberant sound events.
        * Three possible angular speeds for moving sources of approximately 10, 20, or 40deg/sec.
        * Up to three overlapping sound events possible, temporally and spatially.
        * Simultaneous directional interfering sound events with their own temporal activities, static or moving.
        * Realistic spatial ambient noise collected from each room is added to the spatialized sound events, at varying signal-to-noise ratios (SNR) ranging from noiseless (30dB) to noisy (6dB) conditions.

    *Annotations Included:*
        * Each recording in the development set has labels of events and DoAs in a plain csv file with the same filename.
        * Each row in the csv file has a frame number, active class index, event number index, azimuth, and elevation.
        * Frame, class, and clip enumeration begins at 0.
        * Frames correspond to a temporal resolution of 100msec.
        * Azimuth and elevation angles are given in degrees, rounded to the closest integer value, with azimuth and elevation being zero at the front, azimuth :math:`\phi \in [-180^{\circ}, 180^{\circ}]`, and elevation :math:`\\theta \in [-90^{\circ}, 90^{\circ}]`. Note that the azimuth angle is increasing counter-clockwise (:math:`\phi = 90^{\circ}` at the left).
        * The event number index is a unique integer for each event in the recording, enumerating them in the order of appearance. This event identifiers are useful to disentangle directions of co-occuring events through time in the metadata file. The interferers are considered unknown and no activity or direction labels of them are provided with the training datasets.
        * Overlapping sound events are indicated with duplicate frame numbers, and can belong to a different or the same class.

    *Organization*
        * The development dataset is split in training, validation, and test sets.
        * The training set consists of 400 recordings.
        * The validation set consists of 100 recordings.
        * The test set consists of 100 recordings.
        * The evalutation dataset constists of 200 recordings.

    *Please Acknowledge TAU-NIGENS SSE 2021 in Academic Research:*
    If you use this dataset please cite the report on its creation, and the corresponding DCASE2021 task setup:

    .. code-block:: latex

        Archontis Politis, Sharath Adavanne, Daniel Krause, Antoine Deleforge, Prerak Srivastava, and Tuomas Virtanen. A dataset of dynamic reverberant sound scenes with directional interferers for sound event localization and detection. arXiv preprint arXiv:2106.06999, 2021. URL: https://arxiv.org/abs/2106.06999, arXiv:2106.06999.

    *License:*
        * Creative Commons Attribution Non Commercial 4.0 International
"""

import os
from typing import BinaryIO, Optional, TextIO, Tuple

import librosa
import numpy as np
import csv
import json
import glob
import numbers
from itertools import cycle

from soundata import download_utils, core, annotations, io

BIBTEX = """
@article{politis2021dataset,
    author = "Politis, Archontis and Adavanne, Sharath and Krause, Daniel and Deleforge, Antoine and Srivastava, Prerak and Virtanen, Tuomas",
    title = "A Dataset of Dynamic Reverberant Sound Scenes with Directional Interferers for Sound Event Localization and Detection",
    year = "2021",
    journal = "arXiv preprint arXiv:2106.06999",
    eprint = "2106.06999",
    archiveprefix = "arXiv",
    primaryclass = "eess.AS",
    url = "https://arxiv.org/abs/2106.06999"
}
"""

INDEXES = {
    "default": "1.2.0",
    "test": "sample",
    "1.2.0": core.Index(
        filename="tau2021sse_nigens_index_1.2.0.json",
        url="https://zenodo.org/records/11176908/files/tau2021sse_nigens_index_1.2.0.json?download=1",
        checksum="8a3a7348faded292dcdd5e3e072058f5",
    ),
    "sample": core.Index(filename="tau2021sse_nigens_index_1.2.0_sample.json"),
}

REMOTES = {
    "foa_dev": [
        download_utils.RemoteFileMetadata(
            filename="foa_dev.zip",
            url="http://zenodo.org/record/5476980/files/foa_dev.zip?download=1",
            checksum="80648b5f64b1b4a824084560f1334f54",
        ),
        download_utils.RemoteFileMetadata(
            filename="foa_dev.z01",
            url="http://zenodo.org/record/5476980/files/foa_dev.z01?download=1",
            checksum="270a94dc5cd183ea6532c5a3f6e9036c",
        ),
    ],
    "mic_dev": [
        download_utils.RemoteFileMetadata(
            filename="mic_dev.zip",
            url="http://zenodo.org/record/5476980/files/mic_dev.zip?download=1",
            checksum="a5131297547431160b732a3481626c2d",
        ),
        download_utils.RemoteFileMetadata(
            filename="mic_dev.z01",
            url="http://zenodo.org/record/5476980/files/mic_dev.z01?download=1",
            checksum="536a5ba37b0c39f54044932b75acb774",
        ),
    ],
    "foa_eval": download_utils.RemoteFileMetadata(
        filename="foa_eval.zip",
        url="http://zenodo.org/record/5476980/files/foa_eval.zip?download=1",
        checksum="591f8d2b500a671ae34822b4ff1e0889",
    ),
    "mic_eval": download_utils.RemoteFileMetadata(
        filename="mic_eval.zip",
        url="http://zenodo.org/record/5476980/files/mic_eval.zip?download=1",
        checksum="3248aef229ab4e0e0603d7c2269f4f97",
    ),
    "metadata_dev": download_utils.RemoteFileMetadata(
        filename="metadata_dev.zip",
        url="http://zenodo.org/record/5476980/files/metadata_dev.zip?download=1",
        checksum="cd8cd8b4dc9a3e3df91ac55c1ccf73b7",
    ),
    "metadata_eval": download_utils.RemoteFileMetadata(
        filename="metadata_eval.zip",
        url="http://zenodo.org/record/5476980/files/metadata_eval.zip?download=1",
        checksum="11c021253c8b55fd74083bd0a35c2ee4",
    ),
}

LICENSE_INFO = """
Creative Commons Attribution Non Commercial 4.0 International
"""


class Clip(core.Clip):
    """TAU NIGENS SSE 2021 Clip class

    Args:
        clip_id (str): id of the clip
    Attributes:
        audio_path (str): path to the audio file
        tags (soundata.annotation.Tags): tag
        clip_id (str): clip id
        spatial_events (SpatialEvents): sound events with time step, elevation, azimuth, distance, label, clip_number and confidence.
    """

    def __init__(self, clip_id, data_home, dataset_name, index, metadata):
        raise NotImplementedError

    @property
    def audio(self) -> Optional[Tuple[np.ndarray, float]]:
        """The clip's audio
        Returns:
            * np.ndarray - audio signal
            * float - sample rate
        """
        pass

    @core.cached_property
    def spatial_events(self) -> Optional[annotations.SpatialEvents]:
        """The clip's event annotations

        Returns:
            * SpatialEvents with attributes
                * intervals (list): list of size n np.ndarrays of shape (m, 2), with intervals
                    (as floats) in TIME_UNITS in the form [start_time, end_time]
                * intervals_unit (str): intervals unit, one of TIME_UNITS
                * time_step (int, float, or None): the time-step between events
                * elevations (list): list of size n with np.ndarrays with dtype int,
                    indicating the elevation of the sound event per time_step.
                * elevations_unit (str): elevations unit, one of ELEVATIONS_UNITS
                * azimuths (list): list of size n with np.ndarrays with dtype int,
                    indicating the azimuth of the sound event per time_step if moving
                * azimuths_unit (str): azimuths unit, one of AZIMUTHS_UNITS
                * distances (list): list of size n with np.ndarrays with dtype int,
                    indicating the distance of the sound event per time_step if moving
                * distances_unit (str): distances unit, one of DISTANCES_UNITS
                * labels (list): list of event labels (as strings)
                * labels_unit (str): labels unit, one of LABELS_UNITS
                * clip_number_indices (list): list of clip number indices (as strings)
                * confidence (np.ndarray or None): array of confidence values
        """
        pass


@io.coerce_to_bytes_io
def load_audio(fhandle: BinaryIO, sr=24000) -> Tuple[np.ndarray, float]:
    """Load a TAU NIGENS SSE 2021 audio file

    Args:
        fhandle (str or file-like): path or file-like object pointing to an audio file
        sr (int or None): sample rate for loaded audio, 24000 Hz by default.
        If different from file's sample rate it will be resampled on load.
        Use None to load the file using its original sample rate (24000)
    Returns:
        * np.ndarray - the audio signal
        * float - The sample rate of the audio file
    """
    pass


@io.coerce_to_string_io
def load_spatialevents(fhandle: TextIO, dt=0.1) -> annotations.SpatialEvents:
    """Load an TAU NIGENS SSE 2021 annotation file

    Args:
        fhandle (str or file-like): File-like object or path to
            the sound events annotation file
        dt (float): time step
    Raises:
        IOError: if txt_path doesn't exist
    Returns:
        SpatialEvents: sound spatial events annotation data
    """
    pass


@core.docstring_inherit(core.Dataset)
class Dataset(core.Dataset):
    """The TAU NIGENS SSE 2021 dataset"""

    def __init__(self, data_home=None, version="default"):
        raise NotImplementedError

    @core.copy_docs(load_audio)
    def load_audio(self, *args, **kwargs):
        pass

    @core.cached_property
    def _metadata(self):
        # parsing the data from the filenames due to lack of metadata file
        pass
