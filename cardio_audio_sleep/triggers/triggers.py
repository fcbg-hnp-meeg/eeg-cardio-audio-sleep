from __future__ import annotations  # c.f. PEP 563, PEP 649

from typing import TYPE_CHECKING

from byte_triggers import LSLTrigger
from mne_lsl.lsl import StreamInfo, StreamOutlet

from ..eye_link import BaseEyelink
from ..utils._checks import check_type
from ..utils._docs import fill_doc

if TYPE_CHECKING:
    from byte_triggers._base import BaseTrigger

    from ..eye_link import BaseEyelink


@fill_doc
class Trigger:
    """Trigger class combining an hardware trigger and an eye-link system.

    Parameters
    ----------
    trigger : Trigger
        A trigger instance.
    %(eye_link)s
    """

    def __init__(
        self, trigger: BaseTrigger, eye_link: BaseEyelink, instruments: bool = True
    ):
        if isinstance(trigger, LSLTrigger):
            raise RuntimeError(
                "The trigger can not be an LSL trigger as it is incompatible with "
                "multiprocessing."
            )
        self._trigger = trigger
        self._eye_link = eye_link

    def signal(self, value: int) -> None:
        """Send a trigger value.

        Parameters
        ----------
        value : int
            Value sent on the trigger channel.
        """
        self._trigger.signal(value)
        self._eye_link.signal(str(value))

    @property
    def trigger(self):
        """BSL Trigger instance."""
        return self._trigger

    @property
    def eye_link(self):
        return self._eye_link


class TriggerInstrument:
    """Trigger class for sending instrument filenames on an LSL outlet."""

    def __init__(self):
        self._sinfo = StreamInfo(
            name="instruments",
            stype="Markers",
            n_channels=1,
            sfreq=0,
            dtype="string",
            source_id="instruments",
        )
        self._outlet = StreamOutlet(self._sinfo)

    def signal(self, value: str) -> None:
        """Send an instrument filename on the LSL outlet.

        Parameters
        ----------
        value : str
            Value sent on the LSL outlet.
        """
        check_type(value, (str,), "value")
        self._outlet.push_sample([value])

    def close(self) -> None:
        """Close the LSL outlet."""
        try:
            del self._outlet
        except Exception:
            pass

    def __del__(self):  # noqa: D105
        self.close()

    @property
    def sinfo(self) -> StreamInfo:
        """LSL stream info."""
        return self._sinfo

    @property
    def outlet(self) -> StreamOutlet:
        """LSL stream outlet."""
        return self._outlet
