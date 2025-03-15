from flet.core.icon_button import IconButton
from flet.core.icons import Icons
from flet.core.page import Page


class BackButton(IconButton):
    def __init__(self, route: str = ""):
        super().__init__()
        self.icon = Icons.ARROW_BACK
        self.on_click = self.view_pop
        self.route = route

    def view_pop(self, _):
        self.page.views.pop()
        top_view = self.page.views[-1]
        print("Back:"+top_view.route)
        if self.route == "":
            self.page.go(top_view.route)
        else:
            self.page.go(self.route)
