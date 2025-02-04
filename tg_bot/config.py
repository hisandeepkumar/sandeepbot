import sys

# Prevent running sample_config directly
if __name__.endswith("sample_config"):
    print("Error: Please rename 'sample_config.py' to 'config.py' and modify the values inside it.")
    sys.exit(1)


class Config(object):
    LOGGER = True  # Enable logging

    # ======= REQUIRED CONFIGURATION =======
    API_KEY = "7941135502:AAHz-KGvAAoZEhPVgfVKw3zFbkaB0_Pi5rM"  # Bot token (REQUIRED)
    OWNER_ID = 878604830  # Your Telegram user ID (REQUIRED)
    OWNER_USERNAME = "@sigma6375"  # (Optional: Replace with your username)

    # ======= DATABASE CONFIGURATION =======
    SQLALCHEMY_DATABASE_URI = "sqlite:///bot.db"  # SQLite (for simple setups) or replace with PostgreSQL/MySQL URI
    MESSAGE_DUMP = None  # Message backup (Keep None if not needed)
    
    # ======= MODULES & FEATURES =======
    LOAD = []  # Modules to load (Leave empty to load all)
    NO_LOAD = ['translation', 'rss']  # Modules to disable
    WEBHOOK = False  # Use webhook or polling (Keep False for polling)
    URL = None  # Webhook URL (Keep None for polling)

    # ======= PERMISSIONS & ACCESS =======
    SUDO_USERS = [878604830]  # Add more user IDs if you want sudo access
    SUPPORT_USERS = []  # Users who can use GBan but also get banned
    WHITELIST_USERS = []  # Users who won't be banned/kicked by bot

    # ======= EXTRA SETTINGS =======
    DONATION_LINK = None  # Your donation link (If any)
    CERT_PATH = None  # Path for SSL certificate (If using webhook)
    PORT = 5000  # Port for webhook (Keep 5000 for most cases)
    DEL_CMDS = False  # Delete command messages (True/False)
    STRICT_GBAN = False  # Strict Global Ban (Keep False)
    WORKERS = 8  # Number of bot workers (Increase if needed)
    BAN_STICKER = 'CAADAgADOwADPPEcAXkko5EB3YGYAg'  # Banhammer sticker
    ALLOW_EXCL = False  # Allow `!command` along with `/command`


class Production(Config):
    LOGGER = False  # Disable logging in production


class Development(Config):
    LOGGER = True  # Enable logging in development mode
