from database.db_gino import db


class RelatedWishlist(db.Model):
    __tablename__ = 'related_wishlists'

    rw_id = db.Column(db.BigInteger(), primary_key=True)
    user_tg_id = db.Column(db.ForeignKey('users.tg_id'))
    wishlist_id = db.Column(db.ForeignKey('wishlists.id'))
