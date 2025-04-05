from dataclasses import dataclass
from datetime import datetime

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


@dataclass
class DevicesLocationData:
    latitude: float
    longitude: float
    isOld: bool
    position_type: str
    timestamp: int
    location_finished: bool


class DevicesLocation(Column):
    def __init__(self, store: Store, device_id: str):
        super().__init__()
        try:
            self.location = store.devices[device_id].location
        except:
            self.location = None
        print(self.location)
        self.store = store
        self.expand = True
        if self.location is None:
            self.controls = [
                Text("No location data available")
            ]
        else:
            self.data = DevicesLocationData(
                latitude=self.location['latitude'],
                longitude=self.location['longitude'],
                isOld=self.location['isOld'],
                position_type=self.location['positionType'],
                timestamp=self.location['timeStamp'],
                location_finished=self.location['locationFinished']
            )
            dt_object = datetime.fromtimestamp(float(str(self.data.timestamp)[:10]))
            last_updated_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            self.controls = [
                ListTile(
                    leading=Icon(Icons.GPS_FIXED if self.data.position_type == 'GPS' else Icons.SIGNAL_WIFI_4_BAR),
                    title=Text(f"Last updated: {last_updated_time}"),
                    subtitle=Text("old" if self.data.isOld else "new")
                ),
                ListTile(
                    leading=Icon(Icons.PLACE),
                    title=Text(f"Latitude: {self.data.latitude}, Longitude: {self.data.longitude}"),
                    subtitle=Text("Your api key may not have access to your location data")
                ) if not self.store.GOOGLE_API_KEY and not self.store.BAIDU_API_KEY else Column(
                    [
                        ListTile(title=Text("Maps"))
                    ]
                )
            ]
