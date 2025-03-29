import base64

from flet import *
from dataclasses import dataclass

from src.store import Store


class DevicesPage(Column):
    def __init__(self, store: Store, view: View):
        self.store = store
        super().__init__()
        self.controls = [
            ProgressRing()
        ]
        self.scroll = ScrollMode.AUTO
        self.expand = True
        self.alignment = MainAxisAlignment.START
        self.view = view
        self.view.update()

    def did_mount(self):
        self.view.floating_action_button = (
            FloatingActionButton(icon=Icons.REFRESH, on_click=self.refresh_devices))
        self.page.run_task(self.update_devices)
        self.update()

    def will_unmount(self):
        self.view.floating_action_button = None

    async def update_devices(self):
        if self.store.devices is None:
            devices = self.store.api.devices
        else:
            devices = self.store.devices
        self.store.devices = devices
        family_share_devices = []
        owner_devices = []
        for i in devices.keys():
            if not devices[i].data["fmlyShare"]:
                owner_devices.append(DeviceInformationCard(i, devices[i].data, self.store))
            else:
                family_share_devices.append(DeviceInformationCard(i, devices[i].data, self.store))
        self.controls = [
            Text("Owner Devices"),
            Column(owner_devices),
            Text("Family Share Devices"),
            Column(family_share_devices),
        ]
        while True:
            if self.view.floating_action_button is not None:
                self.update()
                break

    def refresh_devices(self, _):
        print("Refreshing devices")
        del self.store.devices
        self.store.devices = None
        self.controls = [
            ProgressRing()
        ]
        self.update()
        self.page.run_task(self.update_devices)


@dataclass
class DeviceInfo:
    device_id: str
    device_display_name: str
    name: str
    device_class: str
    raw_device_model: str
    family_share: bool


class DeviceStatus:
    def __init__(self, battery_level: float, battery_status: str, device_status: str):
        self.battery_level = battery_level
        self.battery_status = battery_status
        self.device_status = device_status

    def get_battery_icon(self):
        if self.battery_level is None:
            return Icons.BATTERY_UNKNOWN
        percent = int(self.battery_level * 7)

        if self.battery_status == "Charging":
            return Icons.BATTERY_CHARGING_FULL
        return battery_icon[percent]


battery_icon = {
    0: Icons.BATTERY_0_BAR,
    1: Icons.BATTERY_1_BAR,
    2: Icons.BATTERY_2_BAR,
    3: Icons.BATTERY_3_BAR,
    4: Icons.BATTERY_4_BAR,
    5: Icons.BATTERY_5_BAR,
    6: Icons.BATTERY_6_BAR,
    7: Icons.BATTERY_FULL,

}

device_icon = {
    "iPhone": Icons.SMARTPHONE,
    "iPad": Icons.TABLET,
    "Watch": Icons.WATCH,
    "Accessory": Icons.DEVICES_OTHER
}


class DeviceInformationCard(Card):
    def __init__(self, device_id: str, raw_data: dict[str, str | bool | int | float], store: Store):
        super().__init__()
        self.device_id = device_id
        self.raw_data = raw_data
        self.store = store
        self.data = DeviceInfo(device_id, self.raw_data["deviceDisplayName"], self.raw_data["name"],
                               self.raw_data["deviceClass"], self.raw_data["rawDeviceModel"],
                               self.raw_data["fmlyShare"])
        self.status = DeviceStatus(self.raw_data["batteryLevel"], self.raw_data["batteryStatus"],
                                   self.raw_data["deviceStatus"])
        device_id_base64 = base64.b64encode(self.device_id.encode()).decode("utf-8")
        self.content = Container(Column(
            controls=[
                ListTile(
                    leading=Icon(device_icon[self.data.device_class]),
                    title=Row(
                        [
                            Text(f"{self.data.name}"),
                            Chip(label=Text("Family Share")) if self.data.family_share else Text("")
                        ]
                    ),
                    subtitle=Column([
                        Text(f"{self.data.device_class} - {self.data.device_display_name}"),
                        Row([
                            Text(f"Status: {self.status.device_status}"),
                            Icon(self.status.get_battery_icon()),
                        ])
                    ]),
                ),
                Row([
                    TextButton("More Information", on_click=lambda _: self.page.go(f"/devices/{device_id_base64}")),
                    TextButton("Play Sound", on_click=self.play_sound),
                    TextButton("Lost Mode", on_click=self.confirm_lost_mode),
                ], alignment=MainAxisAlignment.START)
            ]
        ), padding=10)
        # self.col = {"sm": 6, "md": 4, "xl": 2},

    def play_sound(self, _):
        try:
            self.store.devices[self.device_id].play_sound()
        except Exception as e:
            warning = AlertDialog(content=Text(e.__str__()))
            self.page.open(warning)

    def confirm_lost_mode(self, _):
        def open_lost_mode(_):
            self.page.close(confirm_dialog)
            self.lost_mode(None)

        confirm_dialog = AlertDialog(title=Text("Lost Mode"),
                                     content=Text("Are you sure you want to enable lost mode?"), actions=[
                TextButton("Cancel", on_click=lambda _: self.page.close(confirm_dialog)),
                TextButton("Sure", on_click=open_lost_mode)
            ])
        self.page.open(confirm_dialog)

    def lost_mode(self, _):
        telephone_input = TextField(label="Enter phone number")
        show_message_input = TextField(label="Enter message")

        def enable_lost_mode(_):
            self.store.devices[self.device_id].lost_device(telephone_input.value, show_message_input.value)
            self.page.close(dialog)

        dialog = AlertDialog(title=Text("Lost Mode"), content=Container(Column([
            telephone_input,
            show_message_input
        ], height=110)), actions=[
            TextButton("Cancel", on_click=lambda _: self.page.close(dialog)),
            TextButton("Enable", on_click=enable_lost_mode)
        ])

        self.page.open(dialog)
