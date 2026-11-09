"""TQDM Bar styles
Taken from TQDM community"""
from tqdm import tqdm
__all__ = ["STYLES", "tqdm_neon", "tqdm_modern", "tqdm_retro", "tqdm_compact", "tqdm_minimalistic"]

def tqdm_neon(iterable, desc: str ="Task", colour: str | None = None,
              gui: bool = False, **kwargs):
    """Neon style"""
    return tqdm(
        iterable,
        desc=desc,
bar_format="{desc}: "
"\033[1;36m{percentage:3.0f}%\033[0m |{bar}| {n_fmt}/{total_fmt} "
"[{elapsed}<{remaining}, {rate_fmt}]",
        ascii=" \u2591\u2592\u2593\u2588",
        colour="#00ffcc" if not colour else colour,
        gui=gui,
        **kwargs
    )

def tqdm_modern(iterable, desc: str ="Task", colour: str | None = None,
                gui: bool = False, **kwargs):
    """Modern style"""
    return tqdm(
        iterable,
        desc=desc,
bar_format="{desc}: "
"{percentage:3.0f}% |{bar}| [{elapsed}]",
        ascii=" \u258f\u258e\u258d\u258c\u258b\u258a\u2589\u2588",
        colour="magenta" if not colour else colour,
        gui=gui,
        **kwargs
    )

def tqdm_retro(iterable, desc: str ="Task", colour: str | None = None,
               gui: bool = False, **kwargs):
    """Retro style"""
    return tqdm(
        iterable,
        desc=desc,
bar_format="{desc} [{bar}] ({percentage:3.0f}%)",
        ascii=" =>",
        ncols=80,
        gui=gui,
        colour=colour,
        **kwargs
    )

def tqdm_compact(iterable, desc: str ="Task", colour: str | None = None,
                 gui: bool = False, **kwargs):
    """Compact (without bar) style"""
    return tqdm(
        iterable,
        desc=desc,
bar_format="{desc}: "
"{n}/{total} | [{percentage:.1f}%] | Elapsed: {elapsed}",
        gui=gui,
        colour=colour,
        **kwargs
    )

def tqdm_minimalistic(iterable, desc: str ="Task", colour: str | None = None,
                      gui: bool = False, **kwargs):
    """Minimalistic (Dot) style"""
    return tqdm(
        iterable,
        desc=desc,
bar_format="{desc} {percentage:3.0f}% |{bar}|",
        ascii=" \u2219\u25cf",
        colour="white" if not colour else colour,
        gui=gui,
        **kwargs
    )


# Styles dict
STYLES = {
    "default"      : tqdm,
    "neon"         : tqdm_neon,
    "modern"       : tqdm_modern,
    "retro"        : tqdm_retro,
    "compact"      : tqdm_compact,
    "minimalistic" : tqdm_minimalistic
}
