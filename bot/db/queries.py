import datetime
from datetime import date

from sqlalchemy import and_

from database.models.Item import Item
from database.models.RelatedWishlists import RelatedWishlist
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
        await user.create()
        # try:
        #     await user.create()
        # except UniqueViolationError:
        #     user = await UserCommand.get(tg_id)
        #     await user.update(
        #         username=username,
        #     ).apply()
        #     return user
        return user

    @staticmethod
    async def get(user_tg_id: int) -> User:
        return await User.query.where(User.tg_id == user_tg_id).gino.first()

    @staticmethod
    async def count_user_gifts(user_tg_id: int, wishlist_id: int):
        items = await Item.query.where(and_(Item.buyer_tg_id == user_tg_id,
                                            Item.wishlist_id == wishlist_id)).gino.all()
        return len(items)

    @staticmethod
    async def update(user_tg_id: int, **kwargs):
        user = await UserCommand.get(user_tg_id)
        await user.update(
            **kwargs
        ).apply()
        return user

    @staticmethod
    async def update_name(user_tg_id: int, new_name: str):
        user = await UserCommand.get(user_tg_id)
        return await user.update(name=new_name).apply()

    @staticmethod
    async def get_all_users():
        return await User.query.gino.all()

    @staticmethod
    async def make_inactive(user_tg_id: int):
        user = await UserCommand.get(user_tg_id)
        await user.update(
            is_active=False
        ).apply()


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
    async def update(
            wishlist_id: int,
            **kwargs
    ):
        wishlist = await WishlistCommand.get(wishlist_id)
        await wishlist.update(**kwargs).apply()

    @staticmethod
    async def add_to_related_wishlish(user_tg_id: int, wishlist_id: int):
        is_exists = await RelatedWishlist.query.where(and_(
            RelatedWishlist.user_tg_id == user_tg_id,
            RelatedWishlist.wishlist_id == wishlist_id,
        )).gino.first()
        if not is_exists:
            related_wishlist = RelatedWishlist(
                user_tg_id=user_tg_id,
                wishlist_id=wishlist_id,
            )
            await related_wishlist.create()
        return is_exists

    @staticmethod
    async def get(wishlist_id: int) -> Wishlist:
        return await Wishlist.get(wishlist_id)

    @staticmethod
    async def get_all_parties_wishlists_in_days(days: int = 7):
        today = datetime.date.today()
        wishlists = await Wishlist.query.where(and_(
            Wishlist.is_active.is_(True),
            Wishlist.expiration_date == today + datetime.timedelta(days=days)
        )).gino.all()
        return wishlists

    @staticmethod
    async def get_empty_wishlists_in_days(days: int = 1) -> list[Wishlist]:
        wishlists = await Wishlist.query.where(and_(
            Wishlist.is_active.is_(True),
            Wishlist.created_at + datetime.timedelta(days=days) >= datetime.datetime.now()
        )).gino.all()
        array = list()
        for wishlist in wishlists:
            items = await ItemCommand.get_all_wishlist_items(wishlist.id)
            if len(items) == 0:
                array.append(wishlist)
        return array

    @staticmethod
    async def get_all_related_users(wishlist_id: int) -> list[User]:
        relates: list[RelatedWishlist] = await RelatedWishlist.query.where(RelatedWishlist.wishlist_id == wishlist_id).gino.all()
        users = set()
        for relate in relates:
            users.add(
                await User.query.where(relate.user_tg_id == User.tg_id).gino.first()
            )
        return list(users)

    @staticmethod
    async def get_all_gifts(wishlist_id: int) -> list[int]:
        users_ids = set()
        gifted_items = await Item.query.where(and_(
            Item.buyer_tg_id.is_(not None),
            Item.wishlist_id == wishlist_id
        )).gino.all()
        for item in gifted_items:
            users_ids.add(item.buyer_tg_id)
        return list(users_ids)

    @staticmethod
    async def get_by_hashcode(hashcode: str) -> Wishlist:
        return await Wishlist.query.where(Wishlist.hashcode == hashcode).gino.first()

    @staticmethod
    async def get_all_user_wishlists(user_tg_id: int) -> list[Wishlist]:
        array = await Wishlist.query.where(and_(
            Wishlist.creator_tg_id == user_tg_id,
            Wishlist.expiration_date >= datetime.date.today(),
            Wishlist.is_active.is_(True))
        ).gino.all()

        return array

    @staticmethod
    async def get_related_wishlists(
            user_tg_id: int,
    ) -> list[Wishlist]:
        related_wishlists = await RelatedWishlist.join(Wishlist).select()\
            .where(and_(
                    RelatedWishlist.user_tg_id == user_tg_id,
                    Wishlist.expiration_date >= datetime.date.today(),
                    Wishlist.is_active.is_(True),
        )).gino.all()
        return related_wishlists

    @staticmethod
    async def remove_from_related(
            user_tg_id: int,
            wishlist_id: int,
    ) -> bool:
        related_wishlist = await RelatedWishlist.query.where(and_(
            RelatedWishlist.user_tg_id == user_tg_id,
            RelatedWishlist.wishlist_id == wishlist_id
        )).gino.first()

        if not related_wishlist:
            return False

        await related_wishlist.delete()
        return True

    @staticmethod
    async def make_inactive(wishlist_id: int):
        wishlist = await Wishlist.get(wishlist_id)
        await wishlist.update(is_active=False).apply()
        return wishlist

    @staticmethod
    async def find_by_hashcode(hashcode: str) -> Wishlist | bool:
        wishlist = await Wishlist.query.where(Wishlist.hashcode == hashcode).gino.first()
        if wishlist is None:
            return False
        return wishlist


class ItemCommand:
    @staticmethod
    async def add(
            wishlist_id: int,
            title: str,
            photo_link: str,
            thumb_link: str,
            description: str | None,
            photo_file_id: str | None,
            **kwargs):
        return await Item(
            wishlist_id=wishlist_id,
            title=title,
            photo_link=photo_link,
            thumb_link=thumb_link,
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
    async def gift(
        giver_tg_id: int,
        item_id: int
    ) -> bool:
        item = await Item.get(item_id)
        if item.buyer_tg_id is not None:
            return False
        await item.update(buyer_tg_id=giver_tg_id).apply()
        return True

    @staticmethod
    async def delete(item_id: int):
        item = await Item.get(item_id)
        await item.delete()
        return item

    @staticmethod
    async def item_counter(wishlist_id: int):
        item_counter = len(await Item.query.where(Item.wishlist_id == wishlist_id).gino.all())
        return item_counter

    @staticmethod
    async def update(
            item: Item,
            **kwargs
    ):
        await item.update(
            **kwargs
        ).apply()

    @staticmethod
    async def get_all_items():
        return await Item.query.gino.all()

    @staticmethod
    async def get_user_gifts(user_tg_id: int) -> list[Item]:
        return await Item.query.where(Item.buyer_tg_id == user_tg_id).gino.all()
