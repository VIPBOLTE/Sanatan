class logging(object):
    LOGGER = True

    # this bot sudo users
    sudo_users = "5595153270", "6176582997"
    
    
    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    
class Production(logging):
    LOGGER = True


class Development(logging):
    LOGGER = True
