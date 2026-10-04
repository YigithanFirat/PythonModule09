from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field()
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field()
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(False)

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with AC")

        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if (
            self.signal_strength > 7.0
            and not self.message_received
        ):
            raise ValueError(
                "Strong signals should include received messages"
            )

        return self


def main() -> None:
    alien = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2026, 10, 4, 14, 0, 0),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True
    )

    print("Alien Contact Log Validation")
    print("=" * 40)
    print("Valid contact report:")
    print(f"ID: {alien.contact_id}")
    print(f"Type: {alien.contact_type.value}")
    print(f"Location: {alien.location}")
    print(f"Signal: {alien.signal_strength}/10")
    print(f"Duration: {alien.duration_minutes} minutes")
    print(f"Witnesses: {alien.witness_count}")
    print(f"Message: '{alien.message_received}'")
    print()

    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2026, 10, 4, 15, 0, 0),
            location="Nevada Desert",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=1,
            is_verified=False
        )
    except ValidationError:
        print("=" * 40)
        print("Expected validation error:")
        print("Telepathic contact requires at least 3 witnesses")


if __name__ == "__main__":
    main()
