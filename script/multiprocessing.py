"""Test for suspending and resuming a process."""

import multiprocessing as mp
import time

import psutil
from byte_trigger import ParallelPortTrigger

from cardio_audio_sleep.config.constants import TRIGGERS
from cardio_audio_sleep.tasks import isochronous
from cardio_audio_sleep.utils import generate_sequence, search_ANT_amplifier

if __name__ == "__main__":
    trigger = ParallelPortTrigger("/dev/parport0")

    stream_name = search_ANT_amplifier()
    ecg_ch_name = "AUX7"

    sequence = generate_sequence(20, 0, 10, TRIGGERS)
    delay = 0.5

    process = mp.Process(target=isochronous, args=(trigger, TRIGGERS, sequence, delay))
    process.start()

    psutil_process = psutil.Process(process.pid)
    time.sleep(5)
    psutil_process.suspend()
    time.sleep(2)
    psutil_process.resume()

    process.join()
