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
    model = get_model()
    txt_field_strip.value="\n".join(model['strings_to_strip'])
    txt_field_favourite_dirs.value="\n".join(model['favourite_directories'])
    cb_actually_delete.value = model['actually_delete'] if 'actually_delete' in model else False
    dlg_modal.open = True
    page.update()

def get_model():
    try:
        with open('prefs.json', 'r') as f:
            data = json.load(f)
    except:
        data = default_model.copy()
    return data

def model_add_favourite_path(path):
    model = get_model()
    if path not in model['favourite_directories']:
        model['favourite_directories'].append(path)
    with open('prefs.json', 'w') as f:
        json.dump(model, f, indent=2)

def model_get_last_favourite_dir():
    model = get_model()
    return model['favourite_directories'][0] if len(model['favourite_directories']) > 0 else ''

# ------------------------------- Private -------------------------------

default_model = {
    'description': 'preferences for stable diffusion textfile cleaner',
    'version': 1,
    'strings_to_strip': [
        '_RealESRGAN_x4plus',
        '_GFPGANv1.3_RealESRGAN_x4plus',
    ],
    'favourite_directories': [],
    'actually_delete': False,
    'other': 'other stuff'
}

def close_dlg(e):
    print('close_dlg')
    dlg_modal.open = False
    page.update()


def ok_dlg(e):
    print('ok_dlg', txt_field_strip.value)
    model = get_model()
    model['strings_to_strip'] = txt_field_strip.value.splitlines()
    model['favourite_directories'] = txt_field_favourite_dirs.value.splitlines()
    model['actually_delete'] = cb_actually_delete.value
    with open('prefs.json', 'w') as f:
        json.dump(model, f, indent=2)
    dlg_modal.open = False
    page.update()


txt_field_strip = TextField(
    label="Strip these strings from png filenames",
    multiline=True,
    disabled=False,
    max_lines=3,
    value="",  # fill this in later
)

txt_field_favourite_dirs = TextField(
    label="Favourite directory paths",
    multiline=True,
    disabled=False,
    max_lines=3,
    value="",  # fill this in later
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
