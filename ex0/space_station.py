from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    # Field constraints prevent invalid station telemetry from being stored.
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field()
    is_operational: bool = Field(True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2026, 9, 30, 12, 0, 0),
        is_operational=True
    )
    print("Space Station Data Validation")
    print("=" * 40)
    print("Valid station created")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power:  {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(
        "Status: Status Operational"
        if station.is_operational
        else "Status: Not Operational"
    )
    try:
        # This deliberately exceeds the crew limit to demonstrate validation.
        SpaceStation(
            station_id="ISS002",
            name="Invalid Station",
            crew_size=25,
            power_level=85.0,
            oxygen_level=90.0,
            last_maintenance=datetime(2026, 9, 30, 12, 0, 0),
            is_operational=True
        )
    except ValidationError as error:
        print("=" * 40)
        print("Excpected validation error")
        print(error.errors()[0]["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()
