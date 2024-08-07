from typing import Annotated
from fastapi import Path, APIRouter

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items():
    return [
        "item1",
        'item2'
    ]


@router.get("/latest/")
def get_latest_items():
    return {"item": {"id": 0, "name": "last"}}


@router.get("/{item-id}/")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "item": {
            "id": item_id
        }
    }
