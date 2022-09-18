import flet
from flet import AlertDialog, ElevatedButton, Page, Text, TextButton, Column, Container, colors, TextField, icons, padding

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

def get_strings_to_strip():
    my_data = [
        '_RealESRGAN_x4plus',
        '_GFPGANv1.3_RealESRGAN_x4plus',
    ]
    # return my_data list as string with newlines
    return '\n'.join(my_data)


dlg_modal = AlertDialog(
    modal=True,
    title=Text("Preferences"),
    content=Column(controls=[
        # Text("Do you really want to delete all those files?"),

        TextField(
            label="strip these strings from png filenames",
            multiline=True,
            disabled=False,
            max_lines=10,
            value=get_strings_to_strip(),
        ),

        # Trick dialog to be wider
        Container(
            bgcolor=colors.TRANSPARENT,
            height=1,
            width=500,
        ),
    ]),
    actions=[
        TextButton("Yes", on_click=close_dlg),
        TextButton("No", on_click=close_dlg),
    ],
    actions_alignment="end",
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
