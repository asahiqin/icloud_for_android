import flet

from src.app import App


async def main(page: flet.Page):
    app = App(page)
    await app.init()


flet.app(target=main)
