from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from schemas import Category, ContactCreate, ContactUpdate, ContactResponse


router = APIRouter(prefix="/contacts", tags=["contacts"])

contacts_db: dict[int, dict] = {}
next_id = 1


@router.post("", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    global next_id
    new_contact = {
        "id": next_id,
        **contact.model_dump(),
        "created_at": datetime.now().isoformat(),
    }
    contacts_db[next_id] = new_contact
    next_id += 1
    return new_contact


@router.get("", response_model=list[ContactResponse])
def list_contacts(category: Optional[Category] = None):
    contacts = list(contacts_db.values())
    if category is not None:
        contacts = [c for c in contacts if c["category"] == category]
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    if contact_id not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts_db[contact_id]


@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updates: ContactUpdate):
    if contact_id not in contacts_db:
        raise HTTPException(status_code=404, detail="Contact not found")
    changes = updates.model_dump(exclude_unset=True, exclude_none=True)
    contacts_db[contact_id].update(changes)
    return contacts_db[contact_id]