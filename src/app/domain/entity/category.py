from dataclasses import dataclass
from typing import Optional, Literal

CategoryType = Literal["income", "expense", "saving", "debt"]


@dataclass(frozen=True, slots=True)
class Category:
    id: str
    name: str
    type: CategoryType
    parent_id: Optional[str] = None