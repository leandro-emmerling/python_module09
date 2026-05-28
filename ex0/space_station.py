#!/usr/bin/env python3


from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):
    """SpaceStation model with different validaten fields."""
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    """Run the main program."""
    print("Space Station Data Validation")
    print("========================================")
    valid = SpaceStation(
        station_id="ISS4242",
        name="Interstellar",
        crew_size=12,
        power_level=42.4,
        oxygen_level=82.1,
        last_maintenance=last_maintenance=datetime(2026, 5, 26, 12, 10))
    print("Valid station created:")
    print(f"ID: {valid.station_id}")
    print(f"Name: {valid.name}")
    print(f"Crew: {valid.crew_size} people")
    print(f"Power: {valid.power_level}%")
    print(f"Oxygen: {valid.oxygen_level}%")
    print("Status: ", end="")
    status = "Operational" if valid.is_operational else "Nonoperational"
    print(status)
    print()
    print("========================================")
    try:
        SpaceStation(
            station_id="ISS4242",
            name="Interstellar",
            crew_size=50,
            power_level=42.4,
            oxygen_level=82.1,
            last_maintenance=datetime(2026, 5, 26, 12, 10))
    except ValidationError as e:
        print("Excepted validation error:")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
