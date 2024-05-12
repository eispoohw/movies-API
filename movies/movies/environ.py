import os

SECRET_KEY = os.environ.get("SECRET_KEY", default="")
DEBUG = bool(int(os.environ.get("DEBUG", default="1")))
