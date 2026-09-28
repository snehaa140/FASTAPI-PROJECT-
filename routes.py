from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .database import get_session
from .models import Item, VALID_STATUSES


router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


# --------------------------------------------------
# POST /items
# Create a new item
# --------------------------------------------------

@router.post(
    "",
    response_model=Item,
    status_code=status.HTTP_201_CREATED
)
def create_item(
    item: Item,
    session: Session = Depends(get_session)
):
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# --------------------------------------------------
# GET /items
# Get all items
# --------------------------------------------------

@router.get(
    "",
    response_model=List[Item]
)
def get_items(
    session: Session = Depends(get_session)
):
    items = session.exec(
        select(Item)
    ).all()

    return items


# --------------------------------------------------
# GET /items/{item_id}
# Get one item
# --------------------------------------------------

@router.get(
    "/{item_id}",
    response_model=Item
)
def get_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found."
        )

    return item


# --------------------------------------------------
# PUT /items/{item_id}
# Update an item
# --------------------------------------------------

@router.put(
    "/{item_id}",
    response_model=Item
)
def update_item(
    item_id: int,
    updated_item: Item,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found."
        )

    item.title = updated_item.title
    item.description = updated_item.description
    item.category = updated_item.category
    item.location = updated_item.location
    item.reported_by = updated_item.reported_by
    item.status = updated_item.status

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# --------------------------------------------------
# DELETE /items/{item_id}
# Delete an item
# --------------------------------------------------

@router.delete(
    "/{item_id}"
)
def delete_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found."
        )

    session.delete(item)
    session.commit()

    return {
        "message": f"Item with ID {item_id} deleted successfully."
    }


# --------------------------------------------------
# GET /items/status/{status}
# Filter by status
# --------------------------------------------------

@router.get(
    "/status/{item_status}",
    response_model=List[Item]
)
def get_items_by_status(
    item_status: str,
    session: Session = Depends(get_session)
):
    normalized_status = item_status.strip().title()

    if normalized_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be Lost, Found, or Returned."
        )

    items = session.exec(
        select(Item).where(
            Item.status == normalized_status
        )
    ).all()

    return items


# --------------------------------------------------
# GET /items/category/{category}
# Filter by category
# --------------------------------------------------

@router.get(
    "/category/{category}",
    response_model=List[Item]
)
def get_items_by_category(
    category: str,
    session: Session = Depends(get_session)
):
    items = session.exec(
        select(Item).where(
            Item.category.ilike(category)
        )
    ).all()

    return items