from flet import *

from src.store import Store


class TwoFactorAuthentication(Column):
    def __init__(self, page: Page, store: Store):
        super().__init__()
        self.alignment = MainAxisAlignment.CENTER
        self.page = page
        self.store = store
        self.code = TextField(label="Your 2FA code")
        self.expand = True
        self.controls = [
            Row(
                controls=[
                    Column(
                        controls=[
                            Text("Two-Factor Authentication"),
                            self.code,
                            Button(text="Submit", on_click=self.submit)
                        ],
                        alignment=MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                alignment=MainAxisAlignment.CENTER
            )
        ]

    def submit(self, _):
        api = self.store.api
        code = self.code.value
        self.controls[0].controls = [
            Column(
                [
                    Text("Validating code..."),
                    ProgressRing()
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ]
        self.page.update()
        result = self.store.api.validate_2fa_code(code)
        if result:
            if not api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    dialog = AlertDialog(content=Text("Failed to request trust. You will likely be prompted for the "
                                                      "code again in the coming weeks"))
                    self.page.open(dialog)
            self.page.views.clear()
            self.page.route = "/"
            self.page.update()
        else:
            self.controls[0].controls = [
                Column(
                    [
                        Text("Invalid code. Please try again."),
                        Button(text="Back", on_click=self.back)
                    ],
                    alignment=MainAxisAlignment.CENTER
                )
            ]
            self.page.update()

    def back(self, _):
        self.page.views.pop()
        self.page.views.pop()
        print(self.page.views)
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
