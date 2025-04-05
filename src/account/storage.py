from flet import Container, Column, Text, ResponsiveRow, Colors, Row
from flet.core import border_radius

from src.store import Store


class StorageComponent(Container):
    def __init__(self, store: Store):
        self.store = store
        super().__init__()
        self.storage_bar = ResponsiveRow(spacing=1, height=30)
        self.content = Column(
            [
                Text("Storage Usage"),
                Container(
                    border_radius=border_radius.all(5),
                    bgcolor=Colors.GREY,
                    content=ResponsiveRow(
                        [self.storage_bar]
                    ),
                )
            ]
        )
        self.padding = 20

    def did_mount(self):
        storage = self.store.api.account.storage
        self.storage_bar.col = round(12 * storage.usage.used_storage_in_percent / 100, 4)
        for usage in storage.usages_by_media.values():
            percent = usage.usage_in_bytes / storage.usage.total_storage_in_bytes
            if percent < 0.03:
                percent = 0.03
            self.storage_bar.controls.append(StorageUsageMedia(round(percent, 4), usage.color))
            self.content.controls.append(
                StorageUsageMediaDescription(usage.label, usage.usage_in_bytes / 1024 / 1024 / 1024, usage.color))
        self.update()


class StorageUsageMedia(Container):
    def __init__(self, percent, color):
        super().__init__()
        self.col = percent * 12
        self.bgcolor = f"#{color}"


class StorageUsageMediaDescription(Row):
    def __init__(self, name, usage: float, color):
        super().__init__()
        unit = "GiB"
        if round(usage, 1) == 0:
            usage = usage*1024
            unit = "MiB"
        self.controls = [
            Container(height=8, width=8, bgcolor=f"#{color}"),
            Text(f"{name}: {round(usage, 1)} {unit}"),
        ]
