from flet import *

from src.store import Store


class DevicesInfoPage(Column):
    def __init__(self, store: Store, device_id: str):
        super().__init__()
        self.store = store
        self.device_id = device_id
        self.raw_data = self.store.devices[self.device_id]
        try:
            baUuid = self.raw_data['baUUID']
        except:
            baUuid = "N/A"
        self.controls.append(Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    Tab(text="Location", content=DevicesLocation(store, self.device_id)),
                    Tab(text="Other Info", content=DataTable(
                        columns=[
                            DataColumn(Text("Property")),
                            DataColumn(Text("Value"))
                        ],
                        rows=[
                            DataRow([DataCell(Text("Device ID")), DataCell(Text(f"{self.device_id}"))]),
                            DataRow([DataCell(Text("Device name")), DataCell(Text(f"{self.raw_data['name']}"))]),
                            DataRow(
                                [DataCell(Text("Device type")), DataCell(Text(f"{self.raw_data['deviceClass']}"))]),
                            DataRow([DataCell(Text("Device model display name")),
                                     DataCell(Text(f"{self.raw_data['modelDisplayName']}"))]),
                            DataRow([DataCell(Text("Device display name")),
                                     DataCell(Text(f"{self.raw_data['deviceDisplayName']}"))]),
                            DataRow([DataCell(Text("Device Model")),
                                     DataCell(Text(f"{self.raw_data['rawDeviceModel']}"))]),
                            DataRow([DataCell(Text("Device baUUID")), DataCell(Text(f"{baUuid}"))]),
                        ]
                    )),
                ],
                expand=1,
            )
        )


class DevicesLocation(Column):
    def __init__(self, store: Store, device_id: str):
        super().__init__()
        self.location = store.devices[device_id].location()
        self.controls = [

        ]
