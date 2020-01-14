from typing import Optional

import dataclasses


@dataclasses.dataclass
class Place:
    id: Optional[int]
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    wikidata_id: Optional[str]
