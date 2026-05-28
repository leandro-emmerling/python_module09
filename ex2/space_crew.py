#!/usr/bin/env python3


from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from typing import Optional, List
from datetime import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """CrewMember model with different validation fields."""
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)
    
    
class SpaceMission(BaseModel):
    """SpaceMission model with different validtion fields."""
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., min_length=1, max_length=3650)
    crew: List[CrewMember]
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)
    
    @model_validator(mode='after')
    def check(self) -> 'SpaceMission':
        """Validator to check if the advanced rules are valid."""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'!")
        if (not any(member.rank == Rank.COMMANDER for member in self.crew)
                and not any(member.rank == Rank.CAPTAIN for member in self.crew)):
            raise ValueError(
                "Mission must habe at least one Commander or Captain")
        for member in self.crew:
            count: int = 0
            if member.years_experience >= 5:
                count += 1
        if self.duration_days > 365 and count < (len.member / 2):
            raise ValueError(
                "Long missions need 50%% experienced crew (5+ Years)")
        if any(member.is_active != True for member in self.crew):
            raise ValueError("All crew members must be active!")
        
