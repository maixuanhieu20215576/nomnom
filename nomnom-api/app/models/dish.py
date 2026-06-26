from datetime import datetime
from decimal import Decimal

from geoalchemy2 import Geography
from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, DateTime, Integer, Numeric, Text, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

material_tag_enum = ENUM(
    "pork", "beef", "chicken", "duck", "vegetables", "noodle", "seafood", "rice", "fish", "fruit",
    name="material_tag",
)
taste_tag_enum = ENUM(
    "spicy", "sweet", "bitter", "neutral", "salty", "sour", "savory", "greasy",
    name="taste_tag",
)
country_enum = ENUM(
    "viet", "thai", "korean", "europe", "japan", "china", "other",
    name="country",
)


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    address_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    district: Mapped[str | None] = mapped_column(Text, nullable=True)

    material_tag: Mapped[list[str] | None] = mapped_column(ARRAY(material_tag_enum), nullable=True)
    taste_tag: Mapped[list[str] | None] = mapped_column(ARRAY(taste_tag_enum), nullable=True)
    country: Mapped[str | None] = mapped_column(country_enum, nullable=True)

    food_vector: Mapped[list[float] | None] = mapped_column(Vector(384), nullable=True)

    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
