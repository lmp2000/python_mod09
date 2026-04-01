from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field('planned')
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError(
                'ID must start with "M"'
            )
        if not any(
            c.rank in (Rank.captain, Rank.commander) for c in self.crew
        ):
            raise ValueError(
                'Must have at least one Commander or Captain'
            )
        if self.duration_days > 365:
            experienced = sum(1 for c in self.crew if c.years_experience >= 5)
            if experienced / len(self.crew) < 0.5:
                raise ValueError(...)
        if not all(c.is_active is True for c in self.crew):
            raise ValueError(
                'All crew members must be active'
            )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-06-01T08:00:00",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="CM001",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=45,
                    specialization="Mission Command",
                    years_experience=20,
                ),
                CrewMember(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=10,
                ),
                CrewMember(
                    member_id="CM003",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=28,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ]
        )
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
                f"  - {member.name} ({member.rank.value}) "
                f"- {member.specialization}"
                )
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print('\n' + "=" * 41)

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Doomed Mission",
            destination="Jupiter",
            launch_date="2024-06-01T08:00:00",
            duration_days=100,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="CM001",
                    name="Bob Nobody",
                    rank=Rank.cadet,
                    age=22,
                    specialization="Cleaning",
                    years_experience=0,
                ),
            ]
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == '__main__':
    main()
