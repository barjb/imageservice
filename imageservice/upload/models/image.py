from extensions import db
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from uuid import UUID as _py_uuid
from sqlalchemy.dialects.postgresql import UUID


class Image(db.Model):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[_py_uuid] = mapped_column(UUID())
    filename: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(100))
    url_dither: Mapped[str] = mapped_column(String(100))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
