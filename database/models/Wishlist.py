from datetime import datetime

from database.db_gino import db


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.BigInteger(), primary_key=True)
    hashcode = db.Column(db.String(6), unique=True)
    creator_tg_id = db.Column(db.ForeignKey('users.tg_id'))
    title = db.Column(db.String(64))
    expiration_date = db.Column(db.Date())
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
