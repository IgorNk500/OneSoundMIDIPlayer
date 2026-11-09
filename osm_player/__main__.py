"""OneSound MIDI Player
Play  MIDI (.mid) files only one sound (no SoundFont)

REQUIREMENTS: soundcard, soundfile, numpy, mido, tqdm

Copyright (c) 2026 IgorNk500 (https://github.com/IgorNk500)

+ Homepage: https://github.com/IgorNk500/OneSoundMIDIPlayer
+ Documentation:  https://github.com/IgorNk500/OneSoundMIDIPlayer/wiki
+ Repository: https://github.com/IgorNk500/OneSoundMIDIPlayer
+ Issues: https://github.com/IgorNk500/OneSoundMIDIPlayer/issues
+ Changelog: https://github.com/IgorNk500/OneSoundMIDIPlayer/blob/main/CHANGELOG.md

===== MAIN CLI ENTRY ====="""
import sys
import logging
from argparse import ArgumentParser

# pylint: disable=import-self
from . import play, save
from . import __version__
from ._tqdm_config import TqdmConfig

NAME = "osm_player"


def config_logger(debug: bool):
    """Configure logger. Call `logging.basicConfig`"""
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,

            format="[ {levelname} | {name} ] ({filename}:{lineno}) : {message}",
            style="{"  # Use figure brackets ({}) in format
        )
    else:
        logging.basicConfig(
            level=logging.INFO,

            format="[  {levelname} | {name}  ]: {message}",
            style="{"  # Use figure brackets ({}) in format
        )


def main():
    """Main CLI entry"""
    parser = ArgumentParser(NAME, description="OneSound MIDI Player. "
                                              "Play  MIDI (.mid) files only one sound"
                                              "(no SoundFont). "
                                              "Copyright (c) 2026 IgorNk500 "
                                              "(https://github.com/IgorNk500)"
                            )

    parser.add_argument("sample", type=str, help="path to sample sound file")
    parser.add_argument("midi", type=str, help="path to MIDI file")

    parser.add_argument("--debug", action="store_true", required=False,
                        help="enable debug logging")
    parser.add_argument("-r", "--root-note", type=int, required=False, default=60,
                        help="sample base (root) note in MIDI format. "
                             "default 60 (C4)")
    parser.add_argument("-t", "--tempo-factor", type=float, required=False, default=1.0,
                        help="MIDI playing tempo factor (coefficient)")
    parser.add_argument("-n", "--no-logger", action="store_true", required=False,
                        help="disable logging messages")
    parser.add_argument("-o", "--output", type=str, required=False, default="",
                        help="if stated, path to output sound file. "
                             "if not stated, result will be played")
    parser.add_argument("-p", "--play", action="store_true", required=False,
                        help="use with --output without --play-after. "
                             "Play the result while file writing")
    parser.add_argument("--play-after", action="store_true", required=False,
                        help="use with --output without --play. "
                             "Play the result after operation")
    parser.add_argument("-c", "--colour", type=str, required=False, default="",
                        help="TQDM bar colour")
    parser.add_argument("-s", "--style", type=str, required=False, default="default",
                        help="TQDM bar style (default, neon, modern, retro, compact, minimalistic)")
    parser.add_argument("-g", "--gui", action="store_true", required=False,
                        help="open TQDM bar in GUI")
    parser.add_argument("--no-tqdm", action="store_true", required=False,
                        help="disable TQDM bar")

    print(f"OneSound MIDI Player (PYTHON {NAME}) v{__version__} by IgorNk500")
    args = parser.parse_args()

    if not args.no_logger:
        config_logger(args.debug)

    logger = logging.getLogger()
    logger.debug("===== START =====")
    logger.debug("PROCESSING ARGS: %s", args)

    if args.no_tqdm:
        custom_tqdm = None
    else:
        custom_tqdm = TqdmConfig(
                                 style=args.style,
                                 colour=args.colour,
                                 gui=args.gui
                                )

    try:
        if args.output == "":
            if args.play_after or args.play:
                logger.warning("Output not stated; Skipping --play-after or --play")

            logger.info("Selected play mode")
            play(args.sample, args.midi, args.root_note,
                 custom_tqdm=custom_tqdm)
        elif args.play_after and args.play:
            logger.critical("cannot use --play-after with --play")
            sys.exit(1)
        elif args.play_after:
            logger.info("Selected play after save mode")
            save(args.sample, args.midi, args.output, args.root_note, play_after=True,
                 custom_tqdm=custom_tqdm)
        elif args.play:
            logger.info("Selected play + save mode")
            play(args.sample, args.midi, args.output, args.root_note,
                 custom_tqdm=custom_tqdm)
        else:
            logger.info("Selected save mode")
            save(args.sample, args.midi, args.output, args.root_note, play_after=False,
                 custom_tqdm=custom_tqdm)

    except Exception as e:
        logger.critical(str(e))
        raise e

    logger.debug("===== END =====")


if __name__ == "__main__":
    main()
