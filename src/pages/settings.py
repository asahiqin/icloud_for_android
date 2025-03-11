from flet import *


class SettingsPage(Column):
    def __init__(self):
        super().__init__()
        self.controls = [
            Text("Settings Page")
        ]
