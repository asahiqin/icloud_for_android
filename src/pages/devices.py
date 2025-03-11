from uu import decode

from flet import *
from pydantic.dataclasses import dataclass

from src.store import DEBUG_MODE
from src.store import Store
from src.test_data.devices import test_devices


class DevicesPage(Column):
    def __init__(self, store: Store):
        self.store = store
        super().__init__()
        self.controls = [
        ]
        self.scroll = ScrollMode.AUTO
        self.expand = True
        self.alignment = MainAxisAlignment.START

    def did_mount(self):
        self.update_devices()

    def update_devices(self):
        if DEBUG_MODE:
            for i in test_devices:
                self.controls.append(DeviceInformation(i["id"], i))
                self.update()
            self.update()
            return 0
        if self.store.devices is None:
            devices = self.store.api.devices
            self.store.devices = devices
        else:
            devices = self.store.devices
        for i in devices.keys():
            self.controls.append(DeviceInformation(i, devices[i].data))
            self.update()
        self.update()


@dataclass
class DeviceInfo:
    device_id: str
    model_display_name: str
    name: str
    device_class: str
    raw_device_model: str
    family_share: bool


device_icon = {
    "iPhone": Icons.SMARTPHONE,
    "iPad": Icons.TABLET,
    "Watch": Icons.WATCH,
    "Accessory": Icons.DEVICES_OTHER
}


class DeviceInformation(Card):
    def __init__(self, device_id: str, raw_data: dict[str, str | bool | int | float]):
        super().__init__()
        self.device_id = device_id
        self.raw_data = raw_data
        self.data = DeviceInfo(device_id, self.raw_data["modelDisplayName"], self.raw_data["name"],
                               self.raw_data["deviceClass"], self.raw_data["rawDeviceModel"],
                               self.raw_data["fmlyShare"])
        self.content = Column(
            controls=[
                ListTile(
                    leading=Icon(device_icon[self.data.device_class]),
                    title=Row(
                        [
                            Text(f"{self.data.name}"),
                            Chip(label=Text("Family Share")) if self.data.family_share else Text("")
                         ]
                    ),
                    subtitle=Text(f"{self.data.device_class} - {self.data.model_display_name}"),
                )
            ]
        )
        # self.col = {"sm": 6, "md": 4, "xl": 2},
