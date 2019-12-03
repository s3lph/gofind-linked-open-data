from typing import Optional

import dataclasses


@dataclasses.dataclass
class Place:
    id: Optional[int]
    name: str
    lat: float
    lon: float
    wikidata_id: str
