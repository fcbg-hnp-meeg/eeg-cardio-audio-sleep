import time

from bsl import StreamRecorder, StreamPlayer
from bsl.utils import Timer
from bsl.triggers.software import TriggerSoftware
from ecgdetectors import Detectors
from matplotlib import pyplot as plt
from mne import find_events
from mne.io import read_raw_fif

from cardio_audio_sleep import Detector, set_log_level
from cardio_audio_sleep.audio import Tone

set_log_level('DEBUG')


if __name__ == '__main__':  # required on windows PC for multiprocessing
#%% Start a Mock StreamPlayer
    fif = 'C:/Users/Mathieu/Documents/git/cardio-audio-sleep/data/ecg-raw.fif'
    sp = StreamPlayer('StreamPlayer', fif)
    sp.start(blocking=True)

    #%% Create the sound
    sound = Tone(volume=5, frequency=1000)

    #%% Initialize
    recorder = StreamRecorder('C:/Users/Mathieu/Downloads/', fname='test',
                              fif_subdir=False)
    recorder.start()
    time.sleep(0.2)
    trigger = TriggerSoftware(recorder)
    detector = Detector('StreamPlayer', 'ECG')
    timer = Timer()
    audio_timer = Timer()

    #%% Record
    detector.prefill_buffer()
    trigger.signal(2)  # start trigger

    timer.reset()
    while timer.sec() <= 60:
        detector.update_loop()
        pos = detector.new_peaks()
        if pos is not None:
            audio_timer.reset()
            # compute where we are relative to the r-peak
            delay = detector.timestamps_buffer[-1] \
                - detector.timestamps_buffer[pos]
            # aim for sound at +100 ms
            while audio_timer.sec() < 0.1 - delay:
                pass
            trigger.signal(1)  # trigger when the sound is delivered
            sound.play()

    trigger.signal(2)
    time.sleep(0.5)
    trigger.close()
    time.sleep(0.5)
    recorder.stop()

    #%% Stop Mock StreamPlayer
    sp.stop()

    #%% Load file and plot
    fname = 'C:/Users/Mathieu/Downloads/test-StreamPlayer-raw.fif'
    raw = read_raw_fif(fname, preload=True)
    events = find_events(raw, stim_channel='TRIGGER')

    # Retrieve data array
    data = raw.get_data(picks='ECG')[0, :]
    detectors = Detectors(raw.info['sfreq'])
    r_peaks = detectors.swt_detector(data)

    # Plot
    f, ax = plt.subplots(1, 1)
    ax.plot(raw.times, data)
    for ev in events:
        if ev[2] == 1:
            ax.axvline(raw.times[ev[0]], color='yellow')
        if ev[2] == 2:
            ax.axvline(raw.times[ev[0]], color='crimson', linewidth=3)
    for peak in r_peaks:
        ax.axvline(raw.times[peak], color='teal', linestyle='--')