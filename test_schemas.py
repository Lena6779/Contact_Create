from pydantic import ValidationError
from schemas import ContactCreate

# Valid contact
good = ContactCreate(
    first_name="Lena", last_name="Smith",
    email="lena@example.com", category="work",
)
print(good)

# Invalid contact: several rules broken at once
try:
    ContactCreate(
        first_name="", last_name="Smith",
        email="lena.example.com", phone="123", category="school",
    )
except ValidationError as e:
    print(e)
    