import flet
from flet import AlertDialog, ElevatedButton, Page, Text, TextButton, Column, Container, colors

page = None

def set_page(p):
    global page
    page = p

def edit_preferences(e):
    print('edit_preferences')
    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()

def close_dlg(e):
    dlg_modal.open = False
    page.update()

dlg_modal = AlertDialog(
    modal=True,
    title=Text("Please confirm"),
    # content=Text("Do you really want to delete all those files?"),
    content=Column(controls=[
        Text("Do you really want to delete all those files?"),
        Text("Do you really want to delete all those files?"),
        Text("Do you really want to delete all those files?"),
        Text("Do you really want to delete all those files?"),
        Container(
            bgcolor=colors.YELLOW,
            height= 100,
            width= 100,
            ),
    ]),
    actions=[
        TextButton("Yes", on_click=close_dlg),
        TextButton("No", on_click=close_dlg),
    ],
    actions_alignment="end",
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
