from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StopInteractionRequest(BaseModel):
    dish_id: int
    time_spent_on_post_ms: int


class ReactionRequest(BaseModel):
    dish_id: int
    reactioned: bool


class UserDishInteractionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    dish_id: int
    reactioned: bool
    shared: bool
    time_spent_on_post_ms: int
    last_order_at: datetime | None = None
    updated_at: datetime
