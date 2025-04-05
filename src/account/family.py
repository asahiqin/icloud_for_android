from flet import Text, Container, Column
from flet.core.list_tile import ListTile

from src.store import Store


class FamilyComponent(Container):
    def __init__(self, store: Store):
        super().__init__()
        self.store = store
        self.padding = 20
        self.content = Column(
            [
                Text("Family Members"),
            ]
        )

    def did_mount(self):
        family_members = self.store.api.account.family
        for member in family_members:
            self.content.controls.append(
                ListTile(
                    title=Text(member.full_name),
                    subtitle=Text(member.apple_id),
                )
            )
