class Config:
    """Base config."""


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    # Replace with your ImageKit.io credentials
    PUBLIC_KEY = "public_G3UYv7Ch8lAxt7iTIr6+kzoIrZE="
    PRIVATE_KEY = "private_q9EwjveVouVtc42R32Zs03xU0yA="
    URL = "https://ik.imagekit.io/videocreator"
