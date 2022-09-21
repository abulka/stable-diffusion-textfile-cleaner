# How about this for a class based approach to booting a Flet application? Seems to work:

import flet
from flet import Page, Text

class Main:
    def __init__(self):
        self.page = None

    def __call__(self, page: Page):
        self.page = page
        page.title = "Alternative Boot experiment"
        self.add_stuff()

    def add_stuff(self):
        self.page.add(
            Text("Some text", size=20),
        )
        self.page.update()


main = Main()

flet.app(target=main)
