from extensions import db
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String, Integer
from uuid import UUID as _py_uuid
from sqlalchemy.dialects.postgresql import UUID


class DitheredImage(db.Model):
    __tablename__ = "ditheredimage"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[_py_uuid] = mapped_column(UUID())
    channels: Mapped[int] = mapped_column(Integer)
    url_dither: Mapped[str] = mapped_column(String(100))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
