# application/categories/ports.py
from typing import Protocol
from app.domain.entity import Category


class CategoryReader(Protocol):
    async def get_all(self) -> list[Category]: ...
    async def get_by_id(self, category_id: str) -> Category | None: ...
