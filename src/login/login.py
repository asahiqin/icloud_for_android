
from flet import *
from src.store import Store


class Login(Column):
    def __init__(self, store: Store):
        super().__init__()
        self.store = store
        self.account = TextField(label='Account', value=self.store.account)
        self.password = TextField(label='Password',password=True, value=self.store.password)
        self.china_mainland = Checkbox(label='China Mainland', value=self.store.china_mainland_option)
        self.login_button = ElevatedButton(text='Login', on_click=self.login)
        self.remember_data = Checkbox(label='Remember', value=self.store.remember_me_option)
        self.controls = [
            Text('Login'),
            self.account,
            self.password,
            self.china_mainland,
            self.remember_data,
            self.login_button
        ]
        self.alignment = alignment.center

    def login(self, _):
        account = self.account.value
        password = self.password.value
        china_mainland = self.china_mainland.value
        if self.remember_data.value:
            self.store.account = account
            self.store.password = password
            self.store.china_mainland_option = china_mainland
            self.store.remember_me_option = self.remember_data.value
            self.store.store_to_device()
        self.page.go(f'/loading_login/{account}/{password}')
