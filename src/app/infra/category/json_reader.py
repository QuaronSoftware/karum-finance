import json
from pathlib import Path
from app.domain.entity import Category
from app.application.ports import CategoryReader


class JsonCategoryReader(CategoryReader):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        self._cache: list[Category] | None = None
    
    async def get_all(self) -> list[Category]:
        if self._cache is None:
            self._cache = self._load_categories()
        return self._cache
    
    async def get_by_id(self, category_id: str) -> Category | None:
        categories = await self.get_all()
        for category in categories:
            if category.id==category_id:
                return category
    
    def _load_categories(self) -> list[Category]:
        with self._file_path.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)

        return [
            Category(
                id=item["id"],
                name=item["name"],
                type=item["type"],
                parent_id=item.get("parent_id"),
            )
            for item in raw_data
        ]
