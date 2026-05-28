#!/usr/bin/env python3


from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from typing import Optional
from datetime import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """AlienContact model with different validaten fields."""
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check(self) -> 'AlienContact':
        """Validator to check if the advanced rules are valid."""
        if not self.contact_id.startswith("AC"):
            raise ValueError("ID must start with 'AC'!")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact report must be verfieid!")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses!"
                )
        if self.signal_strength > 7 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) must include a received message!"
                )
        return self


def main() -> None:
    """Run the main Program."""
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    valid = AlienContact(
        contact_id="AC_4242",
        timestamp=datetime(2026, 5, 28, 12, 10),
        contact_type=ContactType.RADIO,
        location="42 Heilbronn, Germany",
        signal_strength=9.0,
        duration_minutes=420,
        witness_count=42,
        message_received="Greetings to the evaluator"
        )
    print(f"ID: {valid.contact_id}")
    print(f"Type: {valid.contact_type.value}")
    print(f"Location: {valid.location}")
    print(f"Signal: {valid.signal_strength}/10")
    print(f"Duration: {valid.duration_minutes} minutes")
    print(f"Witnesses: {valid.witness_count}")
    print(f"Message: {valid.message_received}")
    print("\n======================================")
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="ACISS4242",
            timestamp=datetime(2026, 5, 28, 12, 10),
            contact_type=ContactType.TELEPATHIC,
            location="42 Heilbronn, Germany",
            witness_count=2,
            signal_strength=0.0,
            duration_minutes=1400
        )
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        print(msg.replace("Value error, ", ""))


if __name__ == "__main__":
    main()
