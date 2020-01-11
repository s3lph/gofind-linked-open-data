from typing import Optional

import dataclasses


@dataclasses.dataclass
class Image:
    id: Optional[int]
    file: Optional[str]
    mime: Optional[str]
    caption: Optional[str]
    author: Optional[str]
    source: Optional[str]
