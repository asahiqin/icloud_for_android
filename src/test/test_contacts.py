class TestContacts:
    @property
    def me(self):
        return TestMeCard()


class TestMeCard:
    def __init__(self):
        self.first_name = "Asahi"
        self.last_name = "Qin"

    @property
    def photo(self):
        return {'signature': 'signature', 'url': 'picture_url', 'crop': {'x': 0, 'width': 640, 'y': 110, 'height': 640}}