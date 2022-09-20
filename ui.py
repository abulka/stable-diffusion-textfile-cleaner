from time import sleep
import os
import flet
from flet import ListView, Page, Text, TextField, FilledTonalButton, FilledButton, ElevatedButton, icons, colors, Row, ButtonStyle
from flet import FilePicker, FilePickerResultEvent, padding, Container, ProgressRing, Column
from flet import Page, KeyboardEvent, Dropdown, dropdown
from main import list_files, create_two_sets, find_missing_files, add_dir_root_and_txt_extension
import preferences, choose_favourites
from preferences import edit_preferences, model_add_favourite_path, model_get_last_favourite_dir, model_get_last_favourites
from choose_favourites import choose_favourite
from model import model_get_initial_directory
import smokesignal

bad_txt_files = []
chosen_path = None  # user will override later


@smokesignal.on('chose_dir')
def listener_chose_dir(arg):
    print('listener_chose_dir', arg)


def main(page: Page):
    global chosen_path

    page.title = "stable diffusion textfile cleaner"
    page.window_width = 1200
    page.window_center()

    def on_dialog_result(e: FilePickerResultEvent):
        global chosen_path
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)
        if e.path is None:
            print("User cancelled the dialog")
            return
        chosen_path = e.path
        chosen_path = chosen_path.replace('\\', '')
        if '/Volumes/Google Drive/' in chosen_path:
            chosen_path = chosen_path.replace(
                '/Volumes/Google Drive/', f"{os.path.expanduser('~')}/Google Drive/")
        txt1.value = chosen_path
        txt1.update()
        model_add_favourite_path(chosen_path)
        print('chosen_path AFTER dir selection', chosen_path)
        button_scan_clicked(None)

    def button_scan_clicked(e):
        global bad_txt_files, chosen_path

        lv.controls.clear()
        lv.auto_scroll = False
        lv.update()
        result = list_files(txt1.value)
        set1_txt, set2_png = create_two_sets(result)
        print('text files', set1_txt)
        print('png files', set2_png)
        missing_images = find_missing_files(set1_txt, set2_png)
        print('bad orphans', missing_images)
        print('chosen_path', chosen_path)
        if not chosen_path:
            raise Exception(
                'no path chosen - probably an initialisation error')
        bad_txt_files = add_dir_root_and_txt_extension(
            missing_images, dir=chosen_path)
        print(len(bad_txt_files), 'bad txt files')

        for line in bad_txt_files:
            lv.controls.append(
                Text(f"{line}", size=12, font_family="Consolas", selectable=True))
        lv.update()

        txt2.value = num_orphans_calc()
        txt2.update()

    file_picker = FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    pr = ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def pick_directory(_):
        pr.visible = True
        page.update()

        file_picker.initial_directory = model_get_initial_directory()
        file_picker.get_directory_path()
        sleep(3)

        pr.visible = False
        page.update()

    btnPick = ElevatedButton("Choose DIR...",
                             #  on_click=lambda _: file_picker.get_directory_path())
                             on_click=pick_directory)
    btnPickFav = ElevatedButton("Choose Fav...",
                              on_click=lambda _: choose_favourite(None))
    last_favourite_dir = chosen_path = model_get_last_favourite_dir()
    txt1 = TextField(label="DIR", value=last_favourite_dir, expand=True)

    dd = Dropdown(
        width=100,
        options=[
            dropdown.Option("Red"),
            dropdown.Option("Green"),
            dropdown.Option("Blue"),
        ],
    )
    for fav in model_get_last_favourites():
        dd.options.append(dropdown.Option(fav))

    btnScan = FilledTonalButton(
        "Scan", icon=icons.FIND_IN_PAGE, on_click=button_scan_clicked)
    row = Row(spacing=0, controls=[
              btnPick,
              btnPickFav,
              pr,
              txt1,
              # dd, # if want to display dropdown
              btnScan
              ],
              alignment="start")
    page.add(row)

    def buttonDelete_clicked(e):
        lv.controls.clear()
        lv.auto_scroll = True
        num_left_to_delete = len(bad_txt_files)
        for file_path in bad_txt_files:
            if not os.path.exists(file_path):
                print('  File does not exist', file_path)
            else:
                deleted_msg = f"Deleted {file_path}"
                print(deleted_msg)
                # os.remove(file_path)
                lv.controls.append(Text(
                    deleted_msg, size=12, font_family="Consolas", color="red600", selectable=True))
                num_left_to_delete -= 1

                txt2.value = num_orphans_calc(num_left_to_delete)
                txt2.update()
            lv.update()

    def num_orphans_calc(num=None):
        if num is None:
            num = len(bad_txt_files)
        return f"{num} orphaned text files"

    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
    page.add(lv)

    btnDeleteOrphans = ElevatedButton(f"Delete Orphans", icon=icons.DELETE, on_click=buttonDelete_clicked, style=ButtonStyle(
        bgcolor={"focused": colors.RED_200, "": colors.RED_900},
    ))
    txt2 = Text(value=num_orphans_calc(), expand=False)
    container_4 = Container(content=txt2, padding=padding.only(left=10))
    row_prefs = Row(spacing=0, alignment="end", expand=True, controls=[
                    ElevatedButton("Preferences...", icon=icons.SETTINGS, on_click=edit_preferences)])
    row = Row(spacing=0, controls=[
              btnDeleteOrphans,
              container_4,
              row_prefs,
              ], alignment="center")
    page.add(row)

    def on_keyboard(e: KeyboardEvent):
        # keypressed = f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}"
        # print (keypressed)
        if e.key == ',' and e.meta:
            edit_preferences(None)

    page.on_keyboard_event = on_keyboard

    page.update()

    preferences.set_page(page)
    choose_favourites.set_page(page)


flet.app(target=main)
