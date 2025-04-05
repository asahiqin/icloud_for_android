from flet import Column,Page,Text
from flet.core.text_button import TextButton

from flet_permission_handler import PermissionHandler,PermissionType,PermissionStatus


class PermissionPage(Column):
    def __init__(self, page: Page):
        super().__init__()
        permission = PermissionHandler()
        page.overlay.append(permission)
        self.permission = permission
        self.controls = [
            TextButton("Get Storage Permission", on_click=self.get_storage_permission)
        ]

    def did_mount(self):
        if self.check_permission():
            self.page.go("/login")
            return None
        if self.permission.check_permission(PermissionType.MANAGE_EXTERNAL_STORAGE) == PermissionStatus.PERMANENTLY_DENIED:
            self.controls = [
                Text("You have permanently denied the storage permission. Please go to your device settings to grant "
                     "the permission."),
                TextButton("Go to Settings", on_click=lambda _: self.permission.open_app_settings)
            ]

    def get_storage_permission(self, _):
        self.permission.request_permission(PermissionType.MANAGE_EXTERNAL_STORAGE)
        self.check_permission()

    def check_permission(self):
        if not self.permission.check_permission(PermissionType.MANAGE_EXTERNAL_STORAGE) == PermissionStatus.GRANTED:
            return False

