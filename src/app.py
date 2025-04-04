import base64

import flet
from flet.core.template_route import TemplateRoute

from src.back_button import BackButton
from src.login.login import Login
from src.login.try_login import TryLogin
from src.login.two_factor_auth import TwoFactorAuthentication
from src.navbar import NavBar, page_index_map
from src.pages.devices import DevicesPage
from src.pages.devices_info import DevicesInfoPage
from src.pages.account import AccountPage
from src.pages.settings import SettingsPage
from src.store import Store, FLET_APP_STORAGE_DATA


class RootPage(flet.View):
    def __init__(self, navbar: NavBar):
        super().__init__("/")
        self.navbar = navbar
        self.navbar.on_change = self.handle_navbar_change
        self.content = flet.Placeholder()
        self.controls = [
            flet.Row(
                expand=True,
                controls=[
                    self.navbar,
                    flet.VerticalDivider(),
                    self.content
                ]
            )
        ]
        print("Storage:",FLET_APP_STORAGE_DATA)

    def on_route_change(self, content):
        self.content = content
        self.controls[0].controls.pop()
        self.controls[0].controls.append(self.content)
        self.update()

    def handle_navbar_change(self, e):
        print(self.page)
        self.navbar.selected_index = e.control.selected_index
        self.page.go(page_index_map.inverse[self.navbar.selected_index])
        print(f"Selected index: {self.navbar.selected_index}")
        self.page.update()


class App:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.data = Store(page)
        self.root = RootPage(NavBar())

    async def init(self):
        await self.data.load_from_device()
        self.default_route()

    def default_route(self):
        self.page.views.clear()
        self.page.route = "/login"

        # self.route_change(None)
        self.page.update()

    def route_change(self, _):
        t_route = TemplateRoute(self.page.route)
        print(t_route.route)
        if t_route.match("/"):
            self.page.views.append(
                self.root
            )
            self.page.update()
            self.page.go("/account")
        elif t_route.match("/devices"):
            self.root.on_route_change(
                flet.Row(
                    controls=[DevicesPage(self.data, self.root)],
                    expand=True,
                    alignment=flet.MainAxisAlignment.START
                )
            )
        elif t_route.match("/account"):
            self.root.on_route_change(
                flet.Row(
                    controls=[AccountPage(self.data)],
                    expand=True,
                    alignment=flet.MainAxisAlignment.START
                )
            )
        elif t_route.match("/devices/:device_id_base64/"):
            device_id = base64.b64decode(t_route.device_id_base64).decode('utf-8')
            self.page.views.append(
                flet.View(
                    "/devices/"+t_route.device_id_base64,
                    [DevicesInfoPage(self.data, device_id)],
                    appbar=flet.AppBar(title=flet.Text(f"{self.data.devices[device_id]['name']}"),
                                       leading=BackButton("/devices")),
                )
            )
        elif t_route.match("/settings"):
            self.root.on_route_change(SettingsPage())
        elif t_route.match("/login/"):
            self.page.views.append(
                flet.View(
                    "/login/",
                    [
                        flet.Column(
                            controls=[flet.Row([Login(self.data)], alignment=flet.MainAxisAlignment.CENTER)],
                            alignment=flet.MainAxisAlignment.CENTER,
                            expand=True,
                        ), ]
                )
            )
        elif t_route.match("/loading_login/:account/:password/"):
            self.page.views.append(
                flet.View(
                    f"/loading_login/{t_route.account}/{t_route.password}",
                    [TryLogin(t_route.account, t_route.password, self.data)]
                )
            )
        elif t_route.match("/login/2fa"):
            self.page.views.append(
                flet.View(
                    "/login/2fa",
                    [
                        TwoFactorAuthentication(self.page, self.data)
                    ],
                )
            )

        else:
            self.page.views.clear()
        self.page.update()
