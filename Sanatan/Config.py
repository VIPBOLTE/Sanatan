class Config(object):
    LOGGER = True

    # this bot sudo users
    sudo_users = "5595153270", "6092692622"
    
    
    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
