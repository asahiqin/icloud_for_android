from time import sleep

from src.test.test_account import TestAccount
from src.test.test_contacts import TestContacts
from src.test.test_devices import test_devices


class TestSession:
    def __init__(self):
        print("[DEBUG] Initializing TestSession...")
        self.headers = {}
        self.cookies = {}
        self.params = {}

        self.auth = None

    def get(self, url, params=None, **kwargs):
        print("[DEBUG] GET request to {}".format(url))
        if url == "picture_url":
            return Response(200, "src/test/test.jpeg")

    def post(self, url, data=None, json=None, **kwargs):
        print("[DEBUG] POST request to {}".format(url))


class Response:
    def __init__(self, status_code, path):
        self.status_code = status_code
        self.path = path

    @property
    def content(self) -> bytes:
        file = open(self.path, "rb")
        return file.read()


class TestPyiCloudService:
    def __init__(self, username, password, with_family=True, **kwargs):
        self.username = username
        self.password = password
        self.with_family = with_family
        self.session = TestSession()
        print("[DEBUG] Initializing PyiCloudService...")

    @staticmethod
    def emulate_wait():
        print("[DEBUG] Emulating wait...")
        sleep(1.0)

    @property
    def requires_2fa(self):
        print("[DEBUG] Checking 2FA...")
        self.emulate_wait()
        return False

    def validate_2fa_code(self, code):
        print("[DEBUG] Validating 2FA code...")
        print("[DEBUG] Code: {}".format(code))
        self.emulate_wait()
        if code == "123456":
            return True
        else:
            return False

    @property
    def is_trusted_session(self):
        print("[DEBUG] Checking trusted session...")
        return False

    def trust_session(self):
        print("[DEBUG] Trusting session...")
        self.emulate_wait()
        return True

    @property
    def devices(self):
        print("[DEBUG] Getting devices...")
        self.emulate_wait()
        return test_devices

    @property
    def contacts(self):
        return TestContacts()

    @property
    def account(self):
        return TestAccount()
