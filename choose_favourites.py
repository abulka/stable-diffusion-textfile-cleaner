import json
import flet
from flet import AlertDialog, ElevatedButton, Page, Text, TextButton, Column, Container, colors, TextField, icons, padding
from flet import Checkbox
from model import get_model

page = None


def set_page(p):
    global page
    page = p
    print('set_page (choose fav)', page)


def choose_favourite(e):
    model = get_model()
    txt_field_favourite_dirs.value="\n".join(model['favourite_directories'])
    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()

def close_dlg(e):
    print('close_dlg')
    dlg_modal.open = False
    page.update()

def ok_dlg(e):
    print('ok_dlg', e)
    # TODO get selected item in listview
    dlg_modal.open = False
    page.update()

txt_field_favourite_dirs = TextField(
    label="Favourite directory paths",
    multiline=True,
    disabled=False,
    max_lines=3,
    value="",  # fill this in later
)

dlg_modal = AlertDialog(
    modal=True,
    title=Text("Choose Recent Favourite Path"),
    content=Container(  # Trick dialog to be wider by using a fixed width container
        width=600,
        content=Column(controls=[
            txt_field_favourite_dirs, # TODO add listview here
        ])),
    actions=[
        TextButton("Ok", on_click=ok_dlg),
        TextButton("Cancel", on_click=close_dlg),
    ],
    actions_alignment="end",
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
