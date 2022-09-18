from time import sleep
import os
import flet
from flet import ListView, Page, Text, TextField, FilledTonalButton, FilledButton, ElevatedButton, icons, colors, Row, ButtonStyle
from flet import FilePicker, FilePickerResultEvent, padding, Container, ProgressRing, Column
from main import list_files, create_two_sets, find_missing_files, add_txt_extension, DIR
from preferences import edit_preferences, set_page

bad_txt_files = []
chosen_path = DIR  # user can override later


def main(page: Page):
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
        button_scan_clicked(None)

    def button_scan_clicked(e):
        global bad_txt_files

        lv.controls.clear()
        lv.auto_scroll = False
        result = list_files(txt1.value)
        set1_txt, set2_png = create_two_sets(result)
        print('text files', set1_txt)
        print('png files', set2_png)
        missing_images = find_missing_files(set1_txt, set2_png)
        print('bad orphans', missing_images)
        bad_txt_files = add_txt_extension(missing_images, dir=chosen_path)
        print(len(bad_txt_files), 'bad txt files')

        for line in bad_txt_files:
            lv.controls.append(Text(f"{line}", size=12, font_family="Consolas", selectable=True))
        lv.update()

        txt2.value = num_orphans_calc()
        txt2.update()

    file_picker = FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    pr = ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def pick_directory(_):
        pr.visible = True
        page.update()

        file_picker.get_directory_path()
        sleep(3)

        pr.visible = False
        page.update()


    btnPick = ElevatedButton("Choose DIR...",
                            #  on_click=lambda _: file_picker.get_directory_path())
                             on_click=pick_directory)
    txt1 = TextField(label="DIR", value=DIR, expand=True)
    btnScan = FilledTonalButton(
        "Scan", icon=icons.FIND_IN_PAGE, on_click=button_scan_clicked)
    row = Row(spacing=0, controls=[
              btnPick,
              pr,
              txt1,
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
                lv.controls.append(Text(deleted_msg, size=12, font_family="Consolas", color="red600", selectable=True))
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
    row_prefs = Row(spacing=0, alignment="end", expand=True, controls=[ElevatedButton("Preferences...", icon=icons.SETTINGS, on_click=edit_preferences)])
    row = Row(spacing=0, controls=[
              btnDeleteOrphans,
              container_4,
              row_prefs,
        ], alignment="center")
    page.add(row)

    page.update()

    set_page(page)

flet.app(target=main)
