# How to share the 'page' variable accross modules, based on Python's recommended global state doco
# https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

import flet
from flet import Page
import config
import somemodule

def main(page: Page):
    config.page = page  # set the global page variable in module 'config'
    somemodule.add_stuff()

flet.app(target=main)
