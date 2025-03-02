import asyncio

from flet import *
from pyicloud import PyiCloudService

from src.back_button import BackButton
from src.store import Store


class TryLogin(Column):
    def __init__(self, username, password, store: Store, page: Page):
        super().__init__()
        self.username = username
        self.password = password
        self.store = store
        self.expand = True
        self.alignment = MainAxisAlignment.CENTER
        self.page = page
        self.controls = [
            Row(
                controls=[
                    Column(
                        controls=[
                            ProgressRing(),
                            Text(f"Account: {self.username}"),
                            Text(f"Password: {self.password}"),
                            Text("Logging in...")
                        ],
                        alignment=MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                alignment=MainAxisAlignment.CENTER
            )
        ]

    def did_mount(self):
        self.page.run_task(self.try_login)

    async def try_login(self):
        try:
            self.store.api = PyiCloudService(self.username, self.password,
                                             china_mainland=self.store.china_mainland_option)
            if self.store.api.requires_2fa:
                self.page.go("/login/2fa")
        except KeyError as _:
            self.controls = [
                Text(f"Error to Login: Password or Username is incorrect."),
                Button(text="Back to Login", on_click=self.back)
            ]
            self.update()

    def back(self, _):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)