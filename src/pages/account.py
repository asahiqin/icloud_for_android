import base64
import os.path

import PIL.Image
from flet import *

from src.store import Store, FLET_APP_STORAGE_DATA, FLET_APP_STORAGE_TEMP


class AccountPage(Column):
    def __init__(self, store: Store):
        super().__init__()
        self.store = store
        self.profile = ListTile(
            leading=ProgressRing(width=40, height=40)
            if not os.path.exists(f"{FLET_APP_STORAGE_TEMP}/mecard_cropped.jpg")
            else Image(src=f"{FLET_APP_STORAGE_TEMP}/mecard_cropped.jpg", border_radius=border_radius.all(100), ),
            title=Text("" if not self.store.user_name else self.store.user_name)
        )
        self.plan = Text("")
        self.expand = True
        self.controls = [
            Card(
                content=Container(
                    content=Column(
                        [
                            self.profile,
                            self.plan
                        ],
                    ),
                    padding=20
                ),
            )
        ]

    def did_mount(self):
        if os.path.exists(f"{FLET_APP_STORAGE_DATA}/mecard.jpg") and self.store.photo_crop["height"]:
            self.update_profile("update_profile")
        me = self.store.api.contacts.me
        user_name = me.first_name + " " + me.last_name
        self.store.user_name = user_name
        self.store.store_to_device()
        photo_url = me.photo.get("url")
        photo_crop = me.photo.get("crop")
        self.store.photo_crop = photo_crop
        self.page.run_task(self.download_mecard_photo(photo_url))
        self.page.pubsub.subscribe(self.update_profile)

    def download_mecard_photo(self, photo_url):
        async def download_photo():
            response = self.store.api.session.get(photo_url)
            if response.status_code == 200:
                with open(f"{FLET_APP_STORAGE_DATA}/mecard.jpg", "wb") as f:
                    f.write(response.content)
                self.page.pubsub.send_all("update_profile")

        return download_photo

    def update_profile(self, msg):
        if msg == "update_profile":
            user_name = self.store.user_name
            crop = self.store.photo_crop
            self.profile.title = Text(user_name)
            image = PIL.Image.open(f"{FLET_APP_STORAGE_DATA}/mecard.jpg")
            crop_config = (crop.get("x"), crop.get("y"),
                           crop.get("x") + crop.get("width"), crop.get("y") + crop.get("height"))
            cropped = image.crop(crop_config)
            cropped.save(f"{FLET_APP_STORAGE_TEMP}/mecard_cropped.jpg")
            self.profile.leading = Image(src=f"{FLET_APP_STORAGE_TEMP}/mecard_cropped.jpg",
                                         border_radius=border_radius.all(100), width=50, height=50, fit=ImageFit.COVER)
            self.update()
