from app.shared.database import db


class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
