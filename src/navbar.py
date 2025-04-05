from bidict import bidict
from flet import *
from flet.core.types import OptionalControlEventCallable

page_index_map = bidict({
    "/account": 0,
    "/devices": 1,
    "/settings": 2,
})


class NavBar(NavigationRail):
    def __init__(self):
        super().__init__()
        self.destinations = [
            NavigationRailDestination(
                icon=Icons.ACCOUNT_CIRCLE,
                label="Account",
            ),
            NavigationRailDestination(
                icon=Icons.DEVICES_OTHER,
                label="Devices",
            ),
            NavigationRailDestination(
                icon=Icons.SETTINGS,
                label="Settings",
            ),
        ]
        self.selected_index = 0
        self.label_type = NavigationRailLabelType.ALL
        self.min_width = 100
        self.min_extended_width = 400
        self.group_alignment = -0.9
        self.min_extended_width = 200

    def did_mount(self):
        self.page.on_resized = self.on_resized

    def on_resized(self, _):
        if self.page.width < 800:
            self.extended = False
        else:
            self.extended = True
        self.update()
