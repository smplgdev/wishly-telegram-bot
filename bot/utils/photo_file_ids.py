from bot.config_reader import config

dev = "imba_robot"
prod = "wishlyRobot"

pictures = {
    'create_wishlist': {
        dev: "AgACAgQAAxkBAAIIcmWBa_QF_OFZzDlTp70VdWy8WRjSAAO_MRvDLBBQScDaCb859W0BAAMCAAN5AAMzBA",
        prod: "AgACAgQAAxkBAAIom2WBbXxLfFs_MX1BxnzlglnNneqrAAO_MRvDLBBQ1VEo_7avysUBAAMCAAN5AAMzBA"
    },
    'holiday_atmosphere': {
        dev: "AgACAgQAAxkBAAIIdGWBb91IDLYovfK_JgJe1NptxdAyAAKBxTEbAAEDCFDf6Tt3O93kwAEAAwIAA3kAAzME",
        prod: "AgACAgQAAxkBAAIomWWBbXir-A5fJrQD5mLKPWHe5QypAAKBxTEbAAEDCFASIiygB08wVAEAAwIAA3kAAzME"
    }
}


def get_picture_file_id(name: str) -> str:
    return pictures[name][config.BOT_USERNAME]
