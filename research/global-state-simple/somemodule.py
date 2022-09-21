from flet import Text
import config

def add_stuff():
    config.page.add(
        Text("Some text", size=20),
    )
    config.page.update()
