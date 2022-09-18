import json
import flet
from flet import AlertDialog, ElevatedButton, Page, Text, TextButton, Column, Container, colors, TextField, icons, padding
from flet import Checkbox

page = None


def set_page(p):
    global page
    page = p
    page.dialog = dlg_modal


def edit_preferences(e):
    print('edit_preferences')
    txt_field_strip.value=get_strings_to_strip()
    dlg_modal.open = True
    page.update()


def close_dlg(e):
    print('close_dlg')
    dlg_modal.open = False
    page.update()


def ok_dlg(e):
    print('ok_dlg', txt_field_strip.value)
    data_persist = {
        'description': 'preferences for stable diffusion textfile cleaner',
        'version': 1,
        'strings_to_strip': txt_field_strip.value,
        'other': 'other stuff'
    }
    with open('prefs.json', 'w') as f:
        json.dump(data_persist, f, indent=2)

    dlg_modal.open = False
    page.update()


def get_strings_to_strip():
    try:
        with open('prefs.json', 'r') as f:
            data = json.load(f)
            return data['strings_to_strip']
    except:
        my_data = [
            '_RealESRGAN_x4plus',
            '_GFPGANv1.3_RealESRGAN_x4plus',
        ]
        # return my_data list as string with newlines
        return '\n'.join(my_data)

def get_favourite_directories():
    return ''

txt_field_strip = TextField(
    label="Strip these strings from png filenames",
    multiline=True,
    disabled=False,
    max_lines=3,
    value=get_strings_to_strip(),
)

txt_field_favourite_dirs = TextField(
    label="Favourite directory paths",
    multiline=True,
    disabled=False,
    max_lines=3,
    value=get_favourite_directories(),
)

cb_actually_delete = Checkbox(label="Actually delete files", value=False)

dlg_modal = AlertDialog(
    modal=True,
    title=Text("Preferences"),
    content=Container(  # Trick dialog to be wider by using a fixed width container
        width=600,
        content=Column(controls=[
            cb_actually_delete,
            txt_field_favourite_dirs,
            txt_field_strip,
        ])),
    actions=[
        TextButton("Ok", on_click=ok_dlg),
        TextButton("Cancel", on_click=close_dlg),
    ],
    actions_alignment="end",
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)
