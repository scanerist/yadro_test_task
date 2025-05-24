from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, int_pk, str_uniq

class User(Base):
    __tablename__ = "users"
    id: Mapped[int_pk]
    gender: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str_uniq] = mapped_column(index=True)
    location: Mapped[str]
    picture: Mapped[str] 