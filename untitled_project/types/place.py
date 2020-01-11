from typing import Optional

import dataclasses


@dataclasses.dataclass
class Place:
    id: Optional[int]
    name: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    wikidata_id: Optional[str]
