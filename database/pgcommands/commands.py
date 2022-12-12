from datetime import date

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from database.models.Item import Item
from database.models.User import User
from database.models.Wishlist import Wishlist
from src.utils.random_code_generator import generate_random_code


class UserCommand:
    @staticmethod
    async def add(tg_id: int, name: str, deep_link: str = None, username: str = None):
        user = User(
            tg_id=tg_id,
            deep_link=deep_link,
            name=name,
            username=username)
        try:
            await user.create()
        except UniqueViolationError:
            return await UserCommand.get(tg_id)
        return user

    @staticmethod
    async def get(user_tg_id: int) -> User:
        return await User.query.where(User.tg_id == user_tg_id).gino.first()

    @staticmethod
    async def count_user_gifts(user_tg_id: int):
        items = await Item.query.where(Item.buyer_tg_id == user_tg_id).gino.all()
        return len(items)

    @staticmethod
    async def update_name(user_tg_id: int, new_name: str):
        user = await UserCommand.get(user_tg_id)
        return await user.update(name=new_name).apply()


class WishlistCommand:
    @staticmethod
    async def add(creator_tg_id: int, title: str, expiration_date: date):
        used_hashcode_list = await Wishlist.select("hashcode").gino.all()
        hashcode_is_unique, hashcode = False, ""
        while not hashcode_is_unique:
            hashcode = generate_random_code(4)
            if hashcode not in used_hashcode_list:
                hashcode_is_unique = True
        return await Wishlist(
            hashcode=hashcode,
            creator_tg_id=creator_tg_id,
            title=title,
            expiration_date=expiration_date,
        ).create()

    @staticmethod
    async def get(wishlist_id: int) -> Wishlist:
        return await Wishlist.get(wishlist_id)

    @staticmethod
    async def get_by_hashcode(hashcode: str) -> Wishlist:
        return await Wishlist.query.where(Wishlist.hashcode == hashcode).gino.first()

    @staticmethod
    async def get_all_user_wishlists(user_tg_id: int) -> list[Wishlist]:
        return await Wishlist.query.where(and_(Wishlist.creator_tg_id == user_tg_id,
                                               Wishlist.is_active.is_(True))).gino.all()

    @staticmethod
    async def make_inactive(wishlist_id: int):
        wishlist = await Wishlist.get(wishlist_id)
        await wishlist.update(is_active=False).apply()
        return wishlist

    @staticmethod
    async def find_by_hashcode(hashcode: str):
        wishlist = await Wishlist.query.where(Wishlist.hashcode == hashcode).gino.first()
        if wishlist is None:
            return False
        return wishlist


class ItemCommand:
    @staticmethod
    async def add(wishlist_id: int, title: str, description: str | None, photo_file_id: str | None, **kwargs):
        return await Item(
            wishlist_id=wishlist_id,
            title=title,
            description=description,
            photo_file_id=photo_file_id,
            **kwargs
        ).create()

    @staticmethod
    async def get_all_wishlist_items(wishlist_id: int) -> list[Item]:
        return await Item.query.where(Item.wishlist_id == wishlist_id).order_by(Item.buyer_tg_id.desc()).gino.all()

    @staticmethod
    async def get(item_id: int):
        return await Item.get(item_id)

    @staticmethod
    async def gift(giver_tg_id: int, item_id: int) -> Item | bool:
        item = await Item.get(item_id)
        if giver_tg_id:
            return False
        await item.update(buyer_tg_id=giver_tg_id).apply()
        return item

    @staticmethod
    async def delete(item_id: int):
        item = await Item.get(item_id)
        await item.delete()
        return item
