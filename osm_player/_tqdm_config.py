"""Config dataclass for TQDM"""
from dataclasses import dataclass
from typing import Optional, Iterable

from ._tqdm_styles import STYLES

__all__ = ["TqdmConfig", "STYLES"]

@dataclass
class TqdmConfig:
    """Config dataclass for TQDM"""
    style: str = "default"

    colour: Optional[str] = None
    gui: bool = False

    def get_style(self):
        """Get TQDM class / function by style name
        :returns : TQDM class/ constructor function"""
        return STYLES[self.style]

    def get_tqdm(self, iterable: Iterable, desc: str, **kwargs):
        """Get final TQDM class / constructor function
        :returns : Final TQDM class / constructor function"""
        return self.get_style()(iterable, desc,
                              gui=self.gui, colour=self.colour,
                              **kwargs)

    def __call__(self, iterable: Iterable, desc: str, **kwargs):
        """`tqdm_config()` call"""
        return self.get_tqdm(iterable, desc, **kwargs)
