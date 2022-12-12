from datetime import datetime

from database.db_gino import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), unique=True)
    deep_link = db.Column(db.String(64))

    sex = db.Column(db.String(1))  # w - Woman, m - Man, u - prefer not to say
    age_category = db.Column(db.Integer())
    #  0 - prefer not to say
    #  1 - 14 or less
    #  2 - 15-17
    #  3 - 18-21
    #  4 - 22-25
    #  5 - 26-35
    #  6 - 36 or older
    name = db.Column(db.String(64))
    username = db.Column(db.String(32))
    is_active = db.Column(db.Boolean(), default=True)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
