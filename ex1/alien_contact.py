from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    contact_type: ContactType
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = Field(False)

    @model_validator(mode='after')
    def validate_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError(
                'ID must start with "AC"'
            )
        if self.contact_type == ContactType.physical:
            if not self.is_verified:
                raise ValueError(
                    'If the contact is physical, it must be verified'
                )
        if self.contact_type == ContactType.telepathic:
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                'Message must be received with that signal strength'
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2024-01-15T10:30:00",
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            contact_type=ContactType.radio,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Witnesses: {contact.witness_count}")
        print(f"Message: '{contact.message_received}'\n")
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("=" * 38)

    try:
        AlienContact(
            contact_id="AC001",
            timestamp="2024-01-15T10:30:00",
            location="Dark Side of the Moon",
            signal_strength=5.0,
            duration_minutes=30,
            contact_type=ContactType.telepathic,
            witness_count=1,
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == '__main__':
    main()
