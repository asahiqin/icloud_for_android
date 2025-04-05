import os

import flet
from pyicloud import PyiCloudService
from pyicloud.services.findmyiphone import AppleDevice
from src.test.test_pyicloud import TestPyiCloudService

DEBUG_MODE = False
FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
FLET_APP_STORAGE_TEMP = os.getenv("FLET_APP_STORAGE_TEMP")
iCloudService = PyiCloudService if not DEBUG_MODE else TestPyiCloudService


class Store:
    def __init__(self, page: flet.Page):
        self.password: str = ""
        self.account: str = ""
        self.china_mainland_option: bool = False
        self.remember_me_option: bool = False
        self.page = page
        self.api: PyiCloudService | None = None
        self.devices: dict[str, AppleDevice] | None = None
        self.BAIDU_API_KEY = ""
        self.GOOGLE_API_KEY = ""
        self.user_name: str = ""
        self.photo_crop = {"x": 0, "y": 0, "width": 0, "height": 0}

    def store_to_device(self):
        store_data = [
            {
                "k": "password",
                "v": self.password
            },
            {
                "k": "account",
                "v": self.account
            },
            {
                "k": "china_mainland_option",
                "v": self.china_mainland_option
            },
            {
                "k": "remember_me_option",
                "v": self.remember_me_option
            },
            {
                "k": "BAIDU_API_KEY",
                "v": self.BAIDU_API_KEY
            },
            {
                "k": "GOOGLE_API_KEY",
                "v": self.GOOGLE_API_KEY
            },
            {
                "k": "user_name",
                "v": self.user_name
            },
            {
                "k": "photo_crop",
                "v": self.photo_crop
            }
        ]
        for item in store_data:
            self.page.client_storage.set(item["k"], item["v"])

    async def load_from_device(self):
        async def load_and_set_default(key, default):
            try:
                value = await self.page.client_storage.get_async(key)
                return value if value is not None else default
            except Exception as e:
                print(f"Failed to load {key} from device storage: {e}")
                return default

        self.password = await load_and_set_default("password", "")
        self.account = await load_and_set_default("account", "")
        self.china_mainland_option = await load_and_set_default("china_mainland_option", False)
        self.remember_me_option = await load_and_set_default("remember_me_option", False)
        self.BAIDU_API_KEY = await load_and_set_default("BAIDU_API_KEY", "")
        self.GOOGLE_API_KEY = await load_and_set_default("GOOGLE_API_KEY", "")
        self.user_name = await load_and_set_default("user_name", "")
        self.photo_crop = await load_and_set_default("photo_crop", {"x": 0, "y": 0, "width": 0, "height": 0})

