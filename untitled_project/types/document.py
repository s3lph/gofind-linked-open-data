from typing import Optional

import dataclasses


@dataclasses.dataclass
class Document:
    id: Optional[int]
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]
    text: Optional[str]
    source: Optional[str]
