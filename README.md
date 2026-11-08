<div align="center">
	<h1 style="color: #3081ba">Familiars</h1>
	<!--
	<img src="logo.png" alt="Logo">-->
	<br/>
	<br/>
	Project bages
</div>

***

### MIDI Player without SoundFont. Only one sound
###### *[(Go to changelog)](CHANGELOG.md)*

## Table of contents
1. [Installing](#installing)
2. [Usage](#usage)
3. [Build](#build)
4. [Workflows](#workflows)

## Installing
### Via pip
```bash
python -m pip install onesoundmidi
```

### Via Github Releases
#### For Linux:
```bash
curl https://github.com/IgorNk500/OneSoundMIDIPlayer/releases/latest/setup.sh | bash
```

#### Or for Windows:
Download setup.bat and run it\
**If you want to play via UI, go to [OneSound MIDI Player UI](https://github.com/IgorNk500/OneSoundUI)**

## Usage
...

## Build
### To build the package, run:
```bash
python -m pip install build
python -m build
```
Don't forget to change the config in the `pyproject.toml` file before doing this.\
**All distributions are stored in the `dist` folder**

## Workflows
**This project contains one workflow that:**
+ collects the wheel library,
+ adds it to the release files,
+ and uploads the release to PyPi.

**Also, project contains *pytest* and *pylint* workflows**

## If you encounter any errors, please open [issue](https://github.com/IgorNk500/OneSoundMIDIPlayer/issues/new "New issue") on GitHub.
