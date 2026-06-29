from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

TagField = Literal["material_tag", "taste_tag", "country", "district"]


class TagValueCountCriteria(BaseModel):
    type: Literal["tag_value_count"]
    field: TagField
    value: str
    min_count: int


class DistinctValueCountCriteria(BaseModel):
    type: Literal["distinct_value_count"]
    field: TagField
    min_distinct: int


class ReviewCountCriteria(BaseModel):
    type: Literal["review_count"]
    min_count: int


class ConsecutiveDaysCriteria(BaseModel):
    type: Literal["consecutive_days"]
    min_days: int


AchievementCriteria = Annotated[
    Union[TagValueCountCriteria, DistinctValueCountCriteria, ReviewCountCriteria, ConsecutiveDaysCriteria],
    Field(discriminator="type"),
]


class AchievementCreate(BaseModel):
    title: str
    description: str | None = None
    icon_object_name: str | None = None
    criteria: AchievementCriteria


class AchievementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    icon_object_name: str | None = None
    criteria: AchievementCriteria
    created_at: datetime


class RefreshUserAchievementsResponse(BaseModel):
    unlocked_achievement_ids: list[int]
