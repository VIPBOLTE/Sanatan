{
    "name": "Sanatan",    
    "env": {
        "BOT_TOKEN": {
            "description": "telegram bot token here",
            "required": "@bot_father"
        },        
        "MONGO_URL": {
            "description": "mongo db url here",
            "required": "mongodb.com"
        },
        "BOT_USERNAME": {
            "description": "telegram bot username here without @",
            "required": " "
        },
        "OWNER_USERNAME": {
            "description": "Owner Username without @",
            "required": " "
        },
        "BOT_NAME": {
            "description": "Simple Bot-name. Do not use Modified Text..",
            "required": " "
        },
        "UPDATE_CHNL": {
            "description": "Your Updates Channel without @",
            "required": " "
        },
        "SUPPORT_GRP": {
            "description": "Your Support Group without @",
            "required": " "
        },
        
        "START_IMG": {
            "description": "Start Image For Bot.",
            "required": " "
        },
        
        "API_ID": {
            "description": "telegram api id here",
            "required": " "
        },
        "API_HASH": {
            "description": "telegram api hash here",
            "required": " "
        }
    },
    "addons": [
        {
            "plan": "heroku-postgresql"
        }
    ]
}
