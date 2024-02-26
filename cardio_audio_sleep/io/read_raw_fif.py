from mne import rename_channels
from mne.io import read_raw_fif as mne_read_raw_fif

from .utils import add_annotations_from_events, map_aux


def read_raw_fif(fname):
    """Read raw FIF files saved with BSL StreamRecorder.

    Parameters
    ----------
    fname : file-like
        Path to the -raw.fif file to load.

    Returns
    -------
    raw : Raw
        MNE raw instance.
    """
    raw = mne_read_raw_fif(fname, preload=True)
    raw = map_aux(raw)
    # old eego LSL plugin has upper case channel names
    mapping = {
        "FP1": "Fp1",
        "FPZ": "Fpz",
        "FP2": "Fp2",
        "FZ": "Fz",
        "CZ": "Cz",
        "PZ": "Pz",
        "POZ": "POz",
        "FCZ": "FCz",
        "OZ": "Oz",
        "FPz": "Fpz",
    }
    for key, value in mapping.items():
        try:
            rename_channels(raw.info, {key: value})
        except Exception:
            pass
    raw = add_annotations_from_events(raw)
    return raw
