import json
import flet
from flet import AlertDialog, ElevatedButton, Page, Text, TextButton, Column, Container, colors, TextField, icons, padding, ListView, Row
from flet import Checkbox, ButtonStyle
from flet.border import BorderSide
from flet.buttons import RoundedRectangleBorder
from model import get_model, model_set_initial_directory, model_get_initial_directory

page = None


def set_page(p):
    global page
    page = p

def choose_favourite(e):
    model = get_model()

    style = ButtonStyle(
        color={
            "hovered": colors.WHITE,
            "focused": colors.BLUE,
            "": colors.BLACK,
        },
        bgcolor={"focused": colors.PINK_200, "": colors.YELLOW},
        padding={"hovered": 20},
        overlay_color=colors.TRANSPARENT,
        elevation={"pressed": 0, "": 1},
        animation_duration=500,
        side={
            "": BorderSide(1, colors.BLUE),
            "hovered": BorderSide(2, colors.BLUE),
        },
        shape={
            "hovered": RoundedRectangleBorder(radius=20),
            "": RoundedRectangleBorder(radius=2),
        },
    )

    lv.controls.clear()
    # txt_field_favourite_dirs.value="\n".join(model['favourite_directories'])
    for line in model['favourite_directories']:
        lv.controls.append(
            # Text(f"{line}", size=12, font_family="Consolas", selectable=False))
            # TextButton(text=f"{line}", on_click=chose),
            ElevatedButton(
                content=Row([Text(f"{line}")], alignment="start"),
                width=100,
                on_click=chose,
                data=line  # easier communication with button handler
            )            
        )
    # lv.update()

    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()


def chose(e):
    # print('chose', e.control.text)
    # value = e.control.content.controls[0].value
    value = e.control.data  # easier communication with button handler via 'data' attribute
    print('chose', value)
    model_set_initial_directory(value)
    dlg_modal.open = False
    page.update()
    
def close_dlg(e):
    print('close_dlg')
    dlg_modal.open = False
    page.update()


# def ok_dlg(e):
#     print('ok_dlg', e)
#     # TODO get selected item in listview
#     dlg_modal.open = False
#     page.update()


# txt_field_favourite_dirs = TextField(
#     label="Favourite directory paths",
#     multiline=True,
#     disabled=False,
#     max_lines=3,
#     value="",  # fill this in later
# )
lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

dlg_modal = AlertDialog(
    modal=True,
    title=Text("Choose Recent Favourite Path"),
    content=Container(  # Trick dialog to be wider by using a fixed width container
        width=800,
        content=Column(controls=[
            # txt_field_favourite_dirs, # TODO add listview here
            lv,
        ])),
    actions=[
        # TextButton("Ok", on_click=ok_dlg),
        TextButton("Cancel", on_click=close_dlg),
    ],
    actions_alignment="end",
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
