import flet
from flet.core.template_route import TemplateRoute

from src.login.login import Login
from src.login.try_login import TryLogin
from src.store import Store


class App:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.data = Store(page)

    async def init(self):
        await self.data.load_from_device()
        self.default_route()

    def default_route(self):
        self.page.views.clear()
        self.page.route = "/login"
        self.page.update()

    def route_change(self, _):
        t_route = TemplateRoute(self.page.route)
        if t_route.match("/main"):
            self.page.views.append(
                flet.View(
                    "/main",
                    [
                        flet.Text("Welcome to Flet!")
                    ],
                )
            )
        elif t_route.match("/login"):
            self.page.views.append(
                flet.View(
                    "/login",
                    [
                        flet.Column(
                            controls=[flet.Row([Login(self.data)], alignment=flet.MainAxisAlignment.CENTER)],
                            alignment=flet.MainAxisAlignment.CENTER,
                            expand=True,
                        ),]
                )
            )
        elif t_route.match("/loading_login/:account/:password/"):
            self.page.views.append(
                flet.View(
                    f"/loading_login/{t_route.account}/{t_route.password}",
                    [TryLogin(t_route.account, t_route.password, self.data, self.page)]
                )
            )
        self.page.update()
