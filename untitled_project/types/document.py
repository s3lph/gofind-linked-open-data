from typing import Optional

import dataclasses


@dataclasses.dataclass
class Document:
    id: Optional[int]
    title: str
    author: Optional[str]
    year: int
    text: str
    source: str
