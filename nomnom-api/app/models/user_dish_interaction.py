from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserDishInteraction(Base):
    __tablename__ = "user_dish_interactions"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    dish_id: Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), primary_key=True)
    reactioned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    time_spent_on_post_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    last_order_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
