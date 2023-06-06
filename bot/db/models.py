import sqlalchemy as sa

from db.base import Base


class TimeBasedModel(Base):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now())


class Item(TimeBasedModel):
    __tablename__ = 'items'

    id = sa.Column(sa.BigInteger(), primary_key=True)
    wishlist_id = sa.Column(sa.ForeignKey('wishlists.id'))
    buyer_tg_id = sa.Column(sa.ForeignKey('users.tg_id'))
    title = sa.Column(sa.String(64))
    description = sa.Column(sa.String(512))
    photo_link = sa.Column(sa.String(100))
    price = sa.Column(sa.String(50))
    photo_file_id = sa.Column(sa.String(200))

    thumb_link = sa.Column(sa.String(100))


class RelatedWishlist(TimeBasedModel):
    __tablename__ = 'related_wishlists'

    rw_id = sa.Column(sa.BigInteger(), primary_key=True)
    user_tg_id = sa.Column(sa.ForeignKey('users.tg_id'))
    wishlist_id = sa.Column(sa.ForeignKey('wishlists.id'))


class User(TimeBasedModel):
    __tablename__ = 'users'

    id = sa.Column(sa.BigInteger(), primary_key=True)
    tg_id = sa.Column(sa.BigInteger(), unique=True)
    deep_link = sa.Column(sa.String(64))

    # sex = sa.Column(sa.String(1))  # w - Woman, m - Man, u - prefer not to say

    name = sa.Column(sa.String(64))
    username = sa.Column(sa.String(32))
    is_active = sa.Column(sa.Boolean(), default=True)
    is_admin = sa.Column(sa.Boolean(), default=False)


class Wishlist(TimeBasedModel):
    __tablename__ = 'wishlists'

    id = sa.Column(sa.BigInteger(), primary_key=True)
    is_active = sa.Column(sa.Boolean, default=True)
    hashcode = sa.Column(sa.String(6), unique=True)
    creator_tg_id = sa.Column(sa.ForeignKey('users.tg_id'))
    title = sa.Column(sa.String(64))
    expiration_date = sa.Column(sa.Date())
