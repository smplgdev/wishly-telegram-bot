from aiogram import Router

from . import start, gift_ideas, create_list
from . import return_to_main_menu
from . import my_wishlists
from ...middlewares import update_user_data

main_menu_router = Router()

main_menu_router.include_router(start.main_menu_router)
main_menu_router.include_router(return_to_main_menu.main_menu_router)
main_menu_router.include_router(gift_ideas.main_menu_router)
main_menu_router.include_router(my_wishlists.main_menu_router)
main_menu_router.include_router(create_list.main_menu_router)

main_menu_router.message.middleware(update_user_data.UpdateUserDataMiddleware())
main_menu_router.inline_query.middleware(update_user_data.UpdateUserDataMiddleware())

router = Router()
router.include_router(create_list.router)
router.include_router(gift_ideas.router)
