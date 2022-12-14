from sqlalchemy import func

from database.db_gino import db


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.BigInteger(), primary_key=True)
    hashcode = db.Column(db.String(6), unique=True)
    creator_tg_id = db.Column(db.ForeignKey('users.tg_id'))
    title = db.Column(db.String(64))
    expiration_date = db.Column(db.Date())
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
