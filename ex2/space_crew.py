from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field()
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field()
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field("planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        # Mission identifiers use the "M" prefix for consistent tracking.
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")
        # Every mission needs an authorized leader before launch.
        if not any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        # Long missions require at least half of the crew to be experienced.
        if self.duration_days > 365:
            experienced_count = sum(
                member.years_experience >= 5
                for member in self.crew
            )

            if experienced_count / len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions need at least 50% experienced crew"
                )
        # Inactive members cannot be assigned to an operational mission.
        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    crew = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=42,
            specialization="Mission Command",
            years_experience=15,
            is_active=True
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
            is_active=True
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=30,
            specialization="Engineering",
            years_experience=6,
            is_active=True
        )
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2026, 10, 4, 16, 0, 0),
        duration_days=900,
        crew=crew,
        mission_status="planned",
        budget_millions=2500.0
    )

    print("Space Mission Crew Validation")
    print("=" * 40)
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")

    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) "
            f"- {member.specialization}"
        )
    print()
    try:
        invalid_crew = [
            CrewMember(
                member_id="CM004",
                name="Bob Stone",
                rank=Rank.OFFICER,
                age=40,
                specialization="Engineering",
                years_experience=10,
                is_active=True
            ),
            CrewMember(
                member_id="CM005",
                name="Jane Miller",
                rank=Rank.LIEUTENANT,
                age=38,
                specialization="Navigation",
                years_experience=9,
                is_active=True
            )
        ]

        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Invalid Mission",
            destination="Moon",
            launch_date=datetime(2026, 10, 5, 10, 0, 0),
            duration_days=100,
            crew=invalid_crew,
            mission_status="planned",
            budget_millions=500.0
        )

    except ValidationError as error:
        print("=" * 40)
        print("Expected validation error:")
        print(error.errors()[0]["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()
