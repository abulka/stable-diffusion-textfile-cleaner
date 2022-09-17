from time import sleep
import flet
from flet import ListView, Page, Text, TextField, FilledTonalButton, FilledButton, ElevatedButton, icons, colors, Row, ButtonStyle
from flet import FilePicker, FilePickerResultEvent
from main import list_files, create_two_sets, find_missing_files, add_txt_extension, DIR

bad_txt_files = []

def main(page: Page):
    page.title = "stable diffustion textfile cleaner"

    btnPick = ElevatedButton("Choose DIR...",
        on_click=lambda _: file_picker.get_directory_path())
    txt1 = TextField(label="DIR", value=DIR)
    row = Row(spacing=0, controls=[
              btnPick, 
              txt1], 
        alignment="start")
    page.add(row)

    def on_dialog_result(e: FilePickerResultEvent):
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)
        txt1.value = e.path
        txt1.update()

    def buttonDelete_clicked(e):
        for file_path in bad_txt_files:
            print('Would delete', file_path)
            # os.remove(file_path)

    def button_clicked(e):
        global bad_txt_files

        lv.controls.clear()
        result = list_files(txt1.value)
        set1_txt, set2_png = create_two_sets(result)
        print('text files', set1_txt)
        print('png files', set2_png)
        missing_images = find_missing_files(set1_txt, set2_png)
        print('bad orphans', missing_images)
        bad_txt_files = add_txt_extension(missing_images)
        print(len(bad_txt_files), 'bad txt files')

        for line in bad_txt_files:
            lv.controls.append(Text(f"{line}"))
        lv.update()

    btnScan = FilledTonalButton(
        "Scan", icon=icons.FIND_IN_PAGE, on_click=button_clicked)
    btnDeleteOrphans = ElevatedButton("Delete Orphans", icon=icons.DELETE, on_click=buttonDelete_clicked, style=ButtonStyle(
        bgcolor={"focused": colors.RED_200, "": colors.RED_900},
    ))
    row = Row(spacing=0, controls=[
              btnScan, btnDeleteOrphans], alignment="spaceEvenly")
    page.add(row)

    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    page.add(lv)

    file_picker = FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()



flet.app(target=main)
