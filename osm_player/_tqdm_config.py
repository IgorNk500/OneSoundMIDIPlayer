"""Config dataclass for TQDM"""
from dataclass import dataclass
from typing import Optional

from ._tqdm_styles import STYLES

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

    def get_tqdm(self, iterable, desc: str, **kwargs):
        """Get final TQDM class / constructor function
        :returns : Final TQDM class / constructor function"""
        return self.get_style(iterable, desc,
                              gui=self.gui, colour=self.colour,
                              **kwargs)
