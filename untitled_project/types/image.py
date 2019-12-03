from typing import Optional

import dataclasses


@dataclasses.dataclass
class Image:
    id: Optional[int]
    file: str
    mime: str
    caption: str
    copy: str
    source: str
