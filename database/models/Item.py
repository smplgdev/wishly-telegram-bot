from datetime import datetime

from database.db_gino import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.BigInteger(), primary_key=True)
    wishlist_id = db.Column(db.ForeignKey('wishlists.id'))
    buyer_tg_id = db.Column(db.ForeignKey('users.tg_id'))
    title = db.Column(db.String(64))
    description = db.Column(db.String(512))
    photo_link = db.Column(db.String(100))
    price = db.Column(db.String(50))
    photo_file_id = db.Column(db.String(200))

    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    thumb_link = db.Column(db.String(100))
