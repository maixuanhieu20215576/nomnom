from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Location(BaseModel):
    latitude: float
    longitude: float


MaterialTag = Literal["pork", "beef", "chicken", "duck", "vegetables", "noodle", "seafood", "rice", "fish", "fruit"]
TasteTag = Literal["spicy", "sweet", "bitter", "neutral", "salty", "sour", "savory", "greasy"]
Country = Literal["viet", "thai", "korean", "europe", "japan", "china", "other"]


class DishBase(BaseModel):
    name: str
    description: str
    address_text: str | None = None
    district: str | None = None
    price: Decimal | None = None
    material_tag: list[MaterialTag] | None = None
    taste_tag: list[TasteTag] | None = None
    country: Country | None = None


class DishCreate(DishBase):
    location: Location
    rating: Decimal
    image_object_names: list[str] = []


class DishRead(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location: Location
    food_vector: list[float] | None = None
    avg_rating: Decimal | None = None
    image_urls: list[str] = []
    reactioned: bool = False
    created_at: datetime
    updated_at: datetime


class DishListResponse(BaseModel):
    items: list[DishRead]
    total: int
    page: int
    page_size: int


class RecommendedDishIdsResponse(BaseModel):
    ids: list[int]
    page: int
    page_size: int


class DishJobCreated(BaseModel):
    job_id: int
    status: Literal["pending"] = "pending"


class DishJobStatus(BaseModel):
    job_id: int
    status: Literal["pending", "done", "failed"]
    dish: DishRead | None = None
    error: str | None = None
