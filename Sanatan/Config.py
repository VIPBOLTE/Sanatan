class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5595153270"
    sudo_users = "5595153270", "6092692622"
    GROUP_ID = -1002126989582
    TOKEN = "7167198617:AAF6pOkVfaoW4soxDFf2b8aicrKBMTrXBGU"
    mongo_url = "mongodb+srv://babusona:hinatababy@cluster0.t0lfelh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    VIDEO_URL = ["https://telegra.ph/file/2f56b2568b3f92abcf55e.mp4"]
    SUPPORT_CHAT = "https://t.me/goku_groupz"
    UPDATE_CHAT = "https://t.me/channelz_k"
    BOT_USERNAME = "@Husbandobot"
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
