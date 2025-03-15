from bidict import bidict
from flet import *
from flet.core.types import OptionalControlEventCallable

page_index_map = bidict({
    "/devices": 0,
    "/settings": 1,
})


class NavBar(NavigationRail):
    def __init__(self):
        super().__init__()
        self.destinations = [
            NavigationRailDestination(
                icon=Icons.DEVICES_OTHER,
                label="Devices",
            ),
            NavigationRailDestination(
                icon=Icons.SETTINGS,
                label="Settings",
            )
        ]
        self.selected_index = 0
        self.label_type = NavigationRailLabelType.ALL
        self.min_width = 100
        self.min_extended_width = 400
        self.group_alignment = -0.9