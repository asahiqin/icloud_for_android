import flet
from pyicloud import PyiCloudService
from pyicloud.services.findmyiphone import AppleDevice

from src.test.test_pyicloud import TestPyiCloudService

DEBUG_MODE = False

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
            }
        ]
        for item in store_data:
            self.page.client_storage.set(item["k"], item["v"])

    async def load_from_device(self):
        self.password = await self.page.client_storage.get_async("password")
        self.password = self.password if self.password is not None else ""
        self.account = await self.page.client_storage.get_async("account")
        self.account = self.account if self.account is not None else ""
        self.china_mainland_option = await self.page.client_storage.get_async("china_mainland_option")
        self.china_mainland_option = self.china_mainland_option if self.china_mainland_option is not None else False
        self.remember_me_option = await self.page.client_storage.get_async("remember_me_option")
        self.remember_me_option = self.remember_me_option if self.remember_me_option is not None else False
        self.BAIDU_API_KEY = await self.page.client_storage.get_async("BAIDU_API_KEY")
        self.BAIDU_API_KEY = self.BAIDU_API_KEY if self.BAIDU_API_KEY is not None else ""
        self.GOOGLE_API_KEY = await self.page.client_storage.get_async("GOOGLE_API_KEY")
        self.GOOGLE_API_KEY = self.GOOGLE_API_KEY if self.GOOGLE_API_KEY is not None else ""
