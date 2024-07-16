class logging(object):
    LOGGER = True
    
    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

class Production(logging):
    LOGGER = True

class Development(logging):
    LOGGER = True
