from time import sleep

from src.test.test_devices import test_devices


class TestPyiCloudService:
    def __init__(self, username, password, with_family=True, china_mainland=False):
        self.username = username
        self.password = password
        self.with_family = with_family
        print("[DEBUG] Initializing PyiCloudService...")

    @staticmethod
    def emulate_wait():
        print("[DEBUG] Emulating wait...")
        sleep(1.0)

    @property
    def requires_2fa(self):
        print("[DEBUG] Checking 2FA...")
        self.emulate_wait()
        return True

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
