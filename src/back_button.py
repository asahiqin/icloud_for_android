from flet.core.icon_button import IconButton
from flet.core.icons import Icons
from flet.core.page import Page


class BackButton(IconButton):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.icon = Icons.ARROW_BACK

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)