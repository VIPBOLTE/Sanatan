
class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5595153270"
    sudo_users = "5595153270"
    GROUP_ID = -1002126989582
    TOKEN = "6902253047:AAGFi9KFbAaqZ6Qj6-fpTR2P5TxxV0omHRQ"
    mongo_url = "mongodb+srv://babusona:hinatababy@cluster0.t0lfelh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "https://t.me/goku_groupz"
    UPDATE_CHAT = "https://t.me/channelz_k"
    BOT_USERNAME = "@GOKU_CHATbot"
    api_id = 13220924
    api_hash = "5542f1adb4a900f648c985a6694fc3ed"
    
    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
