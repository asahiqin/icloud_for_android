import flet
from pyicloud import PyiCloudService

from src.app import App


async def main(page: flet.Page):
    app = App(page)
    await app.init()


if __name__ == "__main__":
    flet.app(target=main)
