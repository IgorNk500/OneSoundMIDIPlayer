# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False

"""
Fast sound sampler class, based on custom audio daemon (thread)

Written on Cython
"""
import threading, logging
from time import sleep

import numpy as np
cimport numpy as cnp

import soundfile as sf

# Init NumPy API
cnp.import_array()

from . cimport _Stretch
from ._Stretch import Stretch

cdef class _Sampler:
    cdef public int  buffer_size
    cdef public int  root_note
    cdef public int  num_channels
    cdef public bint is_playing

    cdef public int sample_sr
    cdef cnp.ndarray sample_data

    cdef object active_notes
    cdef object lock # Thread lock
    cdef object thread
    cdef object stretcher

    cdef object logger

    def __cinit__(self, str sample, int root_note, int buffer_size):
        self.logger = logging.getLogger(__name__)

        self.root_note = root_note
        self.active_notes = {}
        self.lock = threading.Lock()
        self.is_playing = True

        self.logger.info("Reading sample ({})".format(sample))
        data, self.sample_sr = sf.read(sample, dtype="float32")
        self.num_channels = 1 if len(data.shape) == 1 else data.shape[1]

        if buffer_size == 0:
            buffer_size = data.shape[0]
        else:
            self.logger.warning("Using custom buffer size. Output sound can be broken")
        self.buffer_size = buffer_size

        # Format sound; Convert np.array to cnp.ndarray[cnp.float32_t, ndim=2, mode="c"]
        self.logger.debug("Formatting sound")
        if len(data.shape) == 1:
            self.sample_data = <cnp.ndarray[cnp.float32_t, ndim=2, mode="c"]>np.require(
                                                                                        data[np.newaxis, :],
                                                                                        dtype=np.float32,
                                                                                        requirements=['C_CONTIGUOUS']
                                                                                       )
        else:
            self.sample_data = <cnp.ndarray[cnp.float32_t, ndim=2, mode="c"]>np.require(
                                                                                        data.T,
                                                                                        dtype=np.float32,
                                                                                        requirements=['C_CONTIGUOUS']
                                                                                       )

        self.logger.debug("Preparing stretcher")
        self.stretcher = Stretch()
        self.stretcher.preset(self.num_channels, self.sample_sr)

        self.logger.debug("Preparing audio daemon (thread)")
        self.thread = threading.Thread(target=self._daemon, daemon=True)

        self.thread.start()
        self.logger.info("AUDIO DAEMON START!")

    def __dealloc__(self):
        self.close()

    # Restart daemon
    cpdef void restart(self):
        if not self.is_playing:
            self.logger.info("Restarting daemon")
            self.thread.start()
            self.logger.info("AUDIO DAEMON RESTARTED!")
        else:
            self.logger.error("Cannot restart daemon because it is not stopped")

    # Enable note
    cpdef void note_on(self, int note, float velocity, float time_factor, bint loop):
        #cdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] data
        #cdef cnp.ndarray[cnp.float32_t, ndim=2, mode="c"] output_data
        if note != self.root_note:
            #with nogil:
            #    input_data = self.sample_data

            self.stretcher.setTransposeSemitones(float(note - self.root_note))
            self.stretcher.setTimeFactor(time_factor)

            with self.lock:
                self.active_notes[note] = {
                    "data":    self.stretcher.process(self.sample_data).T[::-1].T * velocity,
                    "loop":    loop,
                    "pointer": 0
                }
        else:
            with self.lock:
                self.active_notes[note] = {
                    "data":    self.sample_data * velocity,
                    "loop":    loop,
                    "pointer": 0
                }

    # Disable note
    cpdef void note_off(self, int note):
        with self.lock:
            if note in self.active_notes.keys():
                del self.active_notes[note]
            else:
                self.logger.error(f"Cannot disable {note} note. It is inactive")

    # Check note
    cpdef bint playing(self, int note):
        return note in self.active_notes.keys()

    # Daemon; used Memoryview
    cpdef void _daemon(self):
        cdef int take, remaining, i, ch, ptr
        cdef object finished
        cdef float[:, :] buffer # Buffer Memoryview
        cdef float[:, :] d_view # Data (y) Memoryview

        while self.is_playing:
            buffer = np.zeros((self.num_channels, self.buffer_size), dtype=np.float32)
            finished = []

            with self.lock:
                for note, sound in self.active_notes.items():
                    data = sound["data"]
                    ptr =  sound["pointer"]
                    #print("TO PROCESS:", data)

                    remaining = data.shape[1] - ptr

                    with nogil:
                        take = min(self.buffer_size, remaining)

                    if take > 0:
                        d_view = data

                        with nogil:
                            # Mixer
                            for ch in range(self.num_channels):
                                for i in range(take):
                                    buffer[ch, i] += d_view[ch, ptr + i]

                        sound["pointer"] += take

                        if sound["pointer"] >= data.shape[1]:
                            if sound["loop"]:
                                sound["pointer"] = 0
                            else:
                                finished.append(note)
                for note in finished:
                    del self.active_notes[note]

            #np.clip(buffer, -1.0, 1.0, out=buffer)

            # Play sound
            #self.play_func(np.asarray(buffer.T), self.sample_sr)
            from soundcard import default_speaker
            # print("TO PLAY:", y)

            with default_speaker().player(samplerate=self.sample_sr, channels=self.num_channels) as player:
                player.play(buffer.T)
                #sleep(0.01)

    def close(self):
        self.is_playing = False
        self.logger.info("AUDIO DAEMON END!")

###############

# Python realization (wrapper)
class Sampler:
    @property
    def is_playing(self): return self._instance.is_playing

    @property
    def buffer_size(self): return self._instance.buffer_size

    @property
    def root_note(self): return self._instance.root_note

    @property
    def root_key(self): return self._instance.root_note

    @property
    def num_channels(self): return self._instance.num_channels

    @property
    def sr(self): return self._instance.sample_sr

    # Alias
    @property
    def samplerate(self): return self._instance.sample_sr


    def __init__(self, sample_path: str, root_note: int = 60, buffer_size: int = 0):
        self._instance = _Sampler(sample_path, root_note, buffer_size)

    def __dealloc__(self): self._instance.__dealloc__()

    def playing(self, note: int = 60):
        return self._instance.playing(note)

    def note_on(self, note: int = 60, velocity: float = 1.0, time_factor: float = 1.0, loop: bool = False):
        self._instance.note_on(note, velocity, time_factor, loop)

    def note_off(self, note: int = 60):
        self._instance.note_off(note)

    # Safed note disabler
    def safe_note_off(self, note: int = 60):
        if self.playing(note):
            self.note_off(note)
            return True
        return False

    def restart(self):
        self._instance.restart()

    def close(self):
        self._instance.close()
        sleep(0.1)
