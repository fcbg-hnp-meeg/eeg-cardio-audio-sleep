"""Fill docstrings to avoid redundant docstrings in multiple files.

Inspired from mne: https://mne.tools/stable/index.html
Inspired from mne.utils.docs.py by Eric Larson <larson.eric.d@gmail.com>
"""
import sys

# ------------------------- Documentation dictionary -------------------------
docdict = dict()

# ----------------------------------- audio ----------------------------------
docdict[
    "audio_volume"
] = """
volume : list | int | float
    If an int or a float is provided, the sound will use only one channel
    (mono). If a 2-length sequence is provided, the sound will use 2
    channels (stereo). Volume of each channel is given between 0 and 100.
    For stereo, the volume is given as [L, R]."""
docdict[
    "audio_sample_rate"
] = """
sample_rate : int
    Sampling frequency of the sound. The default is 44100 kHz."""
docdict[
    "audio_duration"
] = """
duration : float
    Duration of the sound. The default is 0.1 second."""

# ----------------------------------- tasks ----------------------------------
docdict[
    "task_verbose"
] = """
verbose : bool
    If True, a timer is logged with the info level every second."""
docdict[
    "trigger"
] = """
trigger : Trigger
    A combination of a BSL trigger instance and of a mock or real eye-link."""
docdict[
    "volume"
] = """
volume : float
    Sound volume between 0 (mute) and 100."""
docdict[
    "sequence"
] = """
sequence : array
    Sequence of stimulus/omissions.
    1 corresponds to a stound stimulus. 2 corresponds to an omission."""

# --------------------------------- eye-tracker ------------------------------
docdict[
    "eye_link"
] = """
eye_link : Eyelink
    Eyelink class which communicates with the Eye-Tracker device."""

# ------------------------- Documentation functions --------------------------
docdict_indented = dict()


def fill_doc(f):
    """
    Fill a docstring with docdict entries.

    Parameters
    ----------
    f : callable
        The function to fill the docstring of. Will be modified in place.

    Returns
    -------
    f : callable
        The function, potentially with an updated __doc__.
    """
    docstring = f.__doc__
    if not docstring:
        return f

    lines = docstring.splitlines()
    indent_count = _indentcount_lines(lines)

    try:
        indented = docdict_indented[indent_count]
    except KeyError:
        indent = " " * indent_count
        docdict_indented[indent_count] = indented = dict()

        for name, docstr in docdict.items():
            lines = [
                indent + line if k != 0 else line
                for k, line in enumerate(docstr.strip().splitlines())
            ]
            indented[name] = "\n".join(lines)

    try:
        f.__doc__ = docstring % indented
    except (TypeError, ValueError, KeyError) as exp:
        funcname = f.__name__
        funcname = docstring.split("\n")[0] if funcname is None else funcname
        raise RuntimeError("Error documenting %s:\n%s" % (funcname, str(exp)))

    return f


def _indentcount_lines(lines):
    """
    Minimum indent for all lines in line list.

    >>> lines = [' one', '  two', '   three']
    >>> indentcount_lines(lines)
    1
    >>> lines = []
    >>> indentcount_lines(lines)
    0
    >>> lines = [' one']
    >>> indentcount_lines(lines)
    1
    >>> indentcount_lines(['    '])
    0
    """
    indent = sys.maxsize
    for line in lines:
        line_stripped = line.lstrip()
        if line_stripped:
            indent = min(indent, len(line) - len(line_stripped))
    if indent == sys.maxsize:
        return 0
    return indent


def copy_doc(source):
    """
    Copy the docstring from another function (decorator).

    The docstring of the source function is prepepended to the docstring of the
    function wrapped by this decorator.

    This is useful when inheriting from a class and overloading a method. This
    decorator can be used to copy the docstring of the original method.

    Parameters
    ----------
    source : function
        Function to copy the docstring from.

    Returns
    -------
    wrapper : function
        The decorated function.

    Examples
    --------
    >>> class A:
    ...     def m1():
    ...         '''Docstring for m1'''
    ...         pass
    >>> class B(A):
    ...     @copy_doc(A.m1)
    ...     def m1():
    ...         ''' this gets appended'''
    ...         pass
    >>> print(B.m1.__doc__)
    Docstring for m1 this gets appended
    """

    def wrapper(func):
        if source.__doc__ is None or len(source.__doc__) == 0:
            raise ValueError("Cannot copy docstring: docstring was empty.")
        doc = source.__doc__
        if func.__doc__ is not None:
            doc += func.__doc__
        func.__doc__ = doc
        return func

    return wrapper
