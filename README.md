<div align="center">
	<h1 style="color: #3081ba">OneSound MIDI Player</h1>
	<!--
	<img src="logo.png" alt="Logo">-->
	<br/>
	<br/>
	<a href="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/release_build.yml"><img src="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/release_build.yml/badge.svg" alt="Build"></a>
	<a href="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/pylint.yml"><img src="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/pylint.yml/badge.svg" alt="PyLint"></a>
	<a href="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/pytest.yml"><img src="https://github.com/IgorNk500/OneSoundMIDIPlayer/actions/workflows/pytest.yml/badge.svg" alt="PyTest"></a>
	<br/>
	<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/pypi/pyversions/osm_player" alt="Supported Python versions"></a>
	<a href="https://github.com/IgorNk500/OneSoundMIDIPlayer"><img src="https://img.shields.io/badge/github-repo-blue?logo=github" alt="GitHub repo"></a>
</div>

***

### MIDI Player without SoundFont. Only one sound
###### *[(Go to changelog)](CHANGELOG.md)*

## Table of contents
1. [Installing](#installing)
2. [Usage](#usage)
3. [Downloading the repo](#downloading-the-repo)
4. [Build](#build)
5. [Workflows](#workflows)

## Installing
### Via pip
```bash
python -m pip install onesoundmidi
```

**If you want to play via UI, go to [OneSound MIDI Player UI](https://github.com/IgorNk500/OneSoundUI)**

## Usage
**Use via `osm_player` or `osmplayer`**

```
osm_player / osmplayer [-h] [--debug]
                       [-r ROOT_NOTE]
                       [-t TEMPO_FACTOR] [-n]
                       [-o OUTPUT] [-p]
                       [--play-after] [-c COLOUR]
                       [-s STYLE] [-g]
                       [--no-tqdm]
                       sample midi

positional arguments:
  sample                path to sample sound
                        file
  midi                  path to MIDI file

options:
  -h, --help            show this help
                        message and exit
  --debug               enable debug logging
  -r, --root-note ROOT_NOTE
                        sample base (root)
                        note in MIDI format.
                        default 60 (C4)
  -t, --tempo-factor TEMPO_FACTOR
                        MIDI playing tempo
                        factor (coefficient)
  -n, --no-logger       disable logging
                        messages
  -o, --output OUTPUT   if stated, path to
                        output sound file.
                        if not stated,
                        result will be
                        played
  -p, --play            use with --output
                        without --play-
                        after. Play the
                        result while file
                        writing
  --play-after          use with --output
                        without --play. Play
                        the result after
                        operation
  -c, --colour COLOUR   TQDM bar colour
  -s, --style STYLE     TQDM bar style
                        (default, neon,
                        modern, retro,
                        compact,
                        minimalistic)
  -g, --gui             open TQDM bar in GUI
  --no-tqdm             disable TQDM bar
```

## Downloading the repo
### Don't forget update submodules after cloning the repository:
```bash
git clone https://github.com/IgorNk500/OneSoundMIDIPlayer.git
cd OneSoundMIDIPlayer
git submodule update --init --recursive
```

## Build
**See [Downloading the repo](#downloading-the-repo)**
### To build the package, run:
```bash
python -m pip install build
python -m build .
```
Don't forget to change the config in the `pyproject.toml` file before doing this.\
**All distributions are stored in the `dist` folder**
#### The project is partially written in Cython. The wheel is valid only for your OS

## Workflows
**This project contains one workflow that:**
+ collects the wheel library,
+ adds it to the release files,
+ and uploads the release to PyPi.

**Also, project contains *pytest* and *pylint* workflows**

## If you encounter any errors, please open [issue](https://github.com/IgorNk500/OneSoundMIDIPlayer/issues/new "New issue") on GitHub.
