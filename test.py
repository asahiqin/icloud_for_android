import asyncio

import flet as ft


async def main(page: ft.Page):
    page.add(ft.Text("Hello, async world!"))
    page.update()

ft.app(main)
