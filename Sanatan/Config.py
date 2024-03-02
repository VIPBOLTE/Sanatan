class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5595153270"
    sudo_users = "5595153270"
    GROUP_ID = -1002082803552
    TOKEN = "6902253047:AAGoxnMLHiRtgiQXf3tmxLmmwd3f9g-Ms9g"
    mongo_url = "mongodb+srv://Bikash:Bikash@bikash.yl2nhcy.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    CHARA_CHANNEL_ID = -1002117539029
    SUPPORT_CHAT = ""ℕ𝔸ℝ𝕌𝕋𝕆 (𝟟𝕥𝕙 ℍ𝕆ℂ𝕂𝔸𝔾𝔼)"
    UPDATE_CHAT = "ℕ𝔸ℝ𝕌𝕋𝕆 (𝟟𝕥𝕙 ℍ𝕆ℂ𝕂𝔸𝔾𝔼) updates"
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
