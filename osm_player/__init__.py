"""OneSound MIDI Player
Play  MIDI (.mid) files only one sound (no SoundFont)

REQUIREMENTS: soundcard, soundfile, numpy, mido, tqdm


MIT License

Copyright (c) 2026 IgorNk500

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import logging
from typing import Optional, Callable

import mido
from mido.midifiles.midifiles import DEFAULT_TEMPO

# pylint: disable=import-self
from .Sampler      import Sampler
from .Stretch      import Stretch
from ._tqdm_config import TqdmConfig

__author__  = "IgorNk500"
__version__ = "1.0"
__all__ = ["Sampler", "Stretch", "TqdmConfig",
           "DEFAULT_TEMPO",
           "play", "save"]


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
def play(sample: str, midi: str, root_note: int = 60, tempo_factor: float = 1.0,
         output: Optional[str] = None,
         custom_tqdm: Optional[TqdmConfig | Callable] = None):
    """Play music
    :arg sample       : Path to sample sound file
    :arg midi         : Path to MIDI file
    :arg root_note    : Sample base (root) note *(in MIDI format)*
    :arg tempo_factor : MIDI playing tempo factor *(coefficient)*
    :arg output       : Output file. if not stated, only play
    :arg custom_tqdm  : Custom TQDM in `TqdmConfig` class. Set None for disable TQDM
    """
    logger = logging.getLogger(__name__)

    logger.info("Reading MIDI (%s)...", midi)
    mid = mido.MidiFile(midi)

    logger.info("Preparing")

    logger.debug("Preparing TQDM")
    if custom_tqdm is None:
        logger.info("TQDM Disabled")
        def custom_tqdm(iterable, **kwargs):
            return iterable

    logger.debug("Preparing Sampler")
    sampler = Sampler(sample, root_note=root_note)

    tempo = int(DEFAULT_TEMPO * tempo_factor) # Base tempo
    time_factor = 0 # time_factor = current_tempo / base_tempo
    logger.info("PLAYING")
    for msg in custom_tqdm(mid.play(meta_messages=True), desc="Playing",
                           total=len(list(mid))):
        # Message processor (match-case statement only in Python >=3.10)
        match msg.type:
            case "note_on":
                sampler.note_on(msg.note, msg.velocity, time_factor=time_factor, loop=False)

            case "note_off":
                sampler.safe_note_off(msg.note) # Safe

            # Meta message "set_tempo"
            case "set_tempo":
                print('\n') # New line after TQDM bar
                logger.debug("Updating tempo: %s", msg.tempo)
                time_factor = msg.tempo / tempo
                logger.debug("New time factor: %s", time_factor)

    logger.debug("Ending Sampler session")
    sampler.close()

    logger.info("SUCCESS!")


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
def save(sample: str, midi: str, output: str, root_note: int = 60, tempo_factor: float = 1.0,
         play_after: bool = False,
         custom_tqdm: Optional[TqdmConfig] = None):
    """Save music
    :arg sample       : Path to sample sound file
    :arg midi         : Path to MIDI file
    :arg output       : Output file. if not stated, only play
    :arg root_note    : Sample base (root) note *(in MIDI format)*
    :arg tempo_factor : MIDI playing tempo factor *(coefficient)*
    :arg play_after   : Play result after saving
    :arg custom_tqdm  : Custom TQDM function / class. Set None for disable TQDM
    :arg tqdm_gui     : Run TQDM in GUI-mode
    :arg tqdm_color   : TQDM bar color"""
    logger = logging.getLogger(__name__)

    logger.info("Reading MIDI (%s)...", midi)
    mid = mido.MidiFile(midi)

    logger.info("Preparing stretcher...")
    #stretcher = Stretch()

    # TODO
