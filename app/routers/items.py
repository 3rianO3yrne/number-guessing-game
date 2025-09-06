from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Union
from uuid import uuid4


router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    item_id: str = Field(default_factory=lambda: uuid4().hex)
    number: int | None = Field(
        title="The number guessed", validate_default=True, le=999
    )


@router.get("/")
async def read_item() -> list[Item]:
    items: list[Item] = [{"id": "Foo", "number": 123}, {"id": "Bar", "number": 142}]
    return items


@router.post("/")
async def create_item(item: Item) -> Item:
    return item


@router.get("/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
